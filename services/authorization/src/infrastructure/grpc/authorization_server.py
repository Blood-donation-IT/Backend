import grpc
from contracts.authorization import authorization_pb2, authorization_pb2_grpc
from src.application.use_cases.register_use_case import RegisterUseCase
from src.application.use_cases.login_use_case import LoginUseCase
from src.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from google.protobuf.timestamp_pb2 import Timestamp

class AuthorizationService(authorization_pb2_grpc.AuthorizationServiceServicer):
    def __init__(self, register_use_case: RegisterUseCase, login_use_case: LoginUseCase, refresh_token_use_case: RefreshTokenUseCase):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case
        self.refresh_token_use_case = refresh_token_use_case

    async def Register(self, request, context: grpc.aio.ServicerContext):
        try:
            if not request.email or not request.password or not request.name:
                raise ValueError("Email, password, and name are required")

            user = await self.register_use_case.execute(
                email=request.email,
                password=request.password,
                name=request.name,
                birth_date=request.birth_date if request.HasField("birth_date") else None
            )
            
            return authorization_pb2.RegisterResponse(
                success=True,
                message="User registered successfully",
                user_id=user.id,
                email=user.email
            )
        except ValueError as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return authorization_pb2.RegisterResponse(
                success=False,
                message=str(e),
                user_id=0,
                email=""
            )
        except Exception as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.INTERNAL)
            return authorization_pb2.RegisterResponse(
                success=False,
                message=f"Internal server error: {str(e)}",
                user_id=0,
                email=""
            )

    async def Login(self, request, context: grpc.aio.ServicerContext):
        try:
            if not request.email or not request.password:
                raise ValueError("Email and password are required")

            user, access_token, refresh_token, expires_at = await self.login_use_case.execute(
                email=request.email,
                password=request.password
            )

            ts = Timestamp()
            ts.FromDatetime(expires_at)

            return authorization_pb2.LoginResponse(
                success=True,
                message="Login successful",
                access_token=access_token,
                refresh_token=refresh_token,
                user_id=user.id,
                email=user.email,
                expires_at=ts
            )
        except ValueError as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return authorization_pb2.LoginResponse(
                success=False,
                message=str(e),
                access_token="",
                refresh_token="",
                user_id=0,
                email=""
            )
        except Exception as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.INTERNAL)
            return authorization_pb2.LoginResponse(
                success=False,
                message=f"Internal server error: {str(e)}",
                access_token="",
                refresh_token="",
                user_id=0,
                email=""
            )

    async def RefreshToken(self, request, context: grpc.aio.ServicerContext):
        try:
            if not request.refresh_token:
                raise ValueError("Refresh token is required")

            access_token, refresh_token, expires_at = await self.refresh_token_use_case.execute(
                refresh_token=request.refresh_token
            )

            ts = Timestamp()
            ts.FromDatetime(expires_at)

            return authorization_pb2.RefreshTokenResponse(
                success=True,
                message="Token refreshed successfully",
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=ts
            )
        except ValueError as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return authorization_pb2.RefreshTokenResponse(
                success=False,
                message=str(e),
                access_token="",
                refresh_token=""
            )
        except Exception as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.INTERNAL)
            return authorization_pb2.RefreshTokenResponse(
                success=False,
                message=f"Internal server error: {str(e)}",
                access_token="",
                refresh_token=""
            )




