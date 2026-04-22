import hashlib
import os

import grpc
from google.auth.transport.requests import Request
from google.oauth2 import id_token

from contracts.authorization import authorization_pb2, authorization_pb2_grpc
from contracts.oauth import oauth_pb2, oauth_pb2_grpc
from contracts.user import user_profile_pb2, user_profile_pb2_grpc


class OAuthService(oauth_pb2_grpc.OAuthServiceServicer):
    def __init__(self) -> None:
        self.authorization_target = (
            f"{os.getenv('AUTHORIZATION_SERVICE_HOST', 'authorization')}:"
            f"{int(os.getenv('AUTHORIZATION_SERVICE_PORT', '50053'))}"
        )
        self.user_target = (
            f"{os.getenv('USER_SERVICE_HOST', 'user-profile')}:"
            f"{int(os.getenv('USER_SERVICE_PORT', '50051'))}"
        )
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID").strip()
        self.password_pepper = os.getenv("OAUTH_PASSWORD")
        if not self.password_pepper:
            raise ValueError("OAUTH_PASSWORD environment variable is not set")

    def _resolve_google_profile(self, request: oauth_pb2.GoogleSignInRequest) -> tuple[str, str, str]:
        payload = id_token.verify_oauth2_token(
            request.id_token,
            Request(),
            self.google_client_id or None,
        )
        email_verified = payload.get("email_verified", False)
        email = (payload.get("email") or request.email).strip().lower()
        if not email or not email_verified:
            raise ValueError("Google account email is missing or not verified")
        name = (payload.get("name") or request.name or "").strip()
        avatar_url = (payload.get("picture") or request.avatar_url or "").strip()
        return email, name, avatar_url

    def _oauth_password(self, email: str) -> str:
        digest = hashlib.sha256(f"{email}:{self.password_pepper}".encode("utf-8")).hexdigest()
        return f"G#{digest[:20]}9aA"

    async def _register_or_login(self, email: str, name: str, password: str) -> tuple[int, str, str, bool]:
        async with grpc.aio.insecure_channel(self.authorization_target) as channel:
            stub = authorization_pb2_grpc.AuthorizationServiceStub(channel)

            register_resp = await stub.Register(
                authorization_pb2.RegisterRequest(
                    name=name or email.split("@")[0],
                    email=email,
                    password=password,
                    confirm_password=password,
                )
            )
            is_new_user = bool(register_resp.success)

            login_resp = await stub.Login(
                authorization_pb2.LoginRequest(email=email, password=password)
            )
            if not login_resp.success:
                raise RuntimeError(login_resp.message or "OAuth login failed")
            return int(login_resp.user_id), login_resp.access_token, login_resp.refresh_token, is_new_user

    async def _sync_profile(self, user_id: int, email: str, name: str, avatar_url: str) -> None:
        async with grpc.aio.insecure_channel(self.user_target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            profile_name = name or email.split("@")[0]
            try:
                await stub.CreateProfile(
                    user_profile_pb2.CreateProfileRequest(
                        user_id=user_id,
                        name=profile_name,
                        email=email,
                        phone="",
                        password_hash="",
                    )
                )
            except grpc.RpcError as e:
                if e.code() != grpc.StatusCode.ALREADY_EXISTS:
                    raise

            try:
                await stub.UpdateProfile(
                    user_profile_pb2.UpdateProfileRequest(
                        user_id=user_id,
                        name=profile_name,
                        avatar_url=avatar_url,
                    )
                )
            except grpc.RpcError:
                return

    async def GoogleSignIn(
        self, request: oauth_pb2.GoogleSignInRequest, context: grpc.aio.ServicerContext
    ) -> oauth_pb2.GoogleSignInResponse:
        try:
            email, name, avatar_url = self._resolve_google_profile(request)
            password = self._oauth_password(email)
            user_id, access_token, refresh_token, is_new_user = await self._register_or_login(
                email=email,
                name=name,
                password=password,
            )
            await self._sync_profile(user_id, email, name, avatar_url)
            return oauth_pb2.GoogleSignInResponse(
                success=True,
                message="OAuth login successful",
                user_id=user_id,
                email=email,
                name=name,
                avatar_url=avatar_url,
                access_token=access_token,
                refresh_token=refresh_token,
                is_new_user=is_new_user,
            )
        except ValueError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except grpc.RpcError as e:
            await context.abort(e.code(), e.details() or "Upstream gRPC call failed")
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))
