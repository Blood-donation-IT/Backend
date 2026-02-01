import grpc
from google.protobuf.timestamp_pb2 import Timestamp
# Импорты твоих контрактов
from contracts.user import user_profile_pb2, user_profile_pb2_grpc
from src.schemas.user import UserProfileResponse, UserRole
from typing import Optional
from datetime import date


def _birth_date_from_proto(proto_user) -> Optional[date]:
    ts = getattr(proto_user, "birth_date", None)
    if not ts or not getattr(ts, "seconds", 0):
        return None
    try:
        dt = ts.ToDatetime()
        return dt.date() if dt else None
    except Exception:
        return None

class UserAuthData:
    """Вспомогательный класс для данных аутентификации (чтобы не тащить Proto наружу)"""
    def __init__(self, user_id, password_hash, roles):
        self.user_id = user_id
        self.password_hash = password_hash
        self.roles = roles

class UserGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def get_profile_by_id(self, user_id: int) -> UserProfileResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            request = user_profile_pb2.GetProfileRequestById(user_id=user_id)
            
            try:
                proto_user = await stub.GetProfileById(request)
                if proto_user.user_id == 0:
                    raise grpc.RpcError(
                        code=grpc.StatusCode.NOT_FOUND,
                        details=f"User profile with id {user_id} not found"
                    )
    
                if proto_user.user_id != user_id:
                    raise grpc.RpcError(
                        code=grpc.StatusCode.NOT_FOUND,
                        details=f"User profile id mismatch: expected {user_id}, got {proto_user.user_id}"
                    )
                return self._map_proto_to_pydantic(proto_user)
            except grpc.RpcError as e:
                raise e

    async def create_user(self, user_id: int, email: str, full_name: str, password_hash: str = "", phone: str = None) -> UserProfileResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            
            # Передаємо user_id з authorization для синхронізації
            request = user_profile_pb2.CreateProfileRequest(
                user_id=user_id,  # Використовуємо user_id з authorization
                full_name=full_name,
                email=email,
                phone=phone or "",
                password_hash=password_hash  
            )
            
            try:
                proto_user = await stub.CreateProfile(request)
                if proto_user.user_id == 0:
                    raise grpc.RpcError(
                        code=grpc.StatusCode.INTERNAL,
                        details="Profile creation failed: returned empty profile"
                    )
                return self._map_proto_to_pydantic(proto_user)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                    try:
                        return await self.get_profile_by_id(user_id)
                    except:
                        raise Exception(f"Profile already exists but cannot be retrieved: {e.details()}")
                raise Exception(f"Failed to create user: {e.details()}")

    async def update_profile(
        self,
        user_id: int,
        full_name: Optional[str] = None,
        blood_type: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> UserProfileResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            request = user_profile_pb2.UpdateProfileRequest(user_id=user_id)
            if full_name is not None:
                request.full_name = full_name
            if blood_type is not None:
                request.blood_type = blood_type
            if avatar_url is not None:
                request.avatar_url = avatar_url
            try:
                response = await stub.UpdateProfile(request)
                if not response.success:
                    raise Exception(response.message or "Update failed")
                return await self.get_profile_by_id(user_id)
            except grpc.RpcError as e:
                raise Exception(f"Failed to update profile: {e.details()}")

    async def get_auth_data_by_email(self, email: str) -> Optional[UserAuthData]:
        """Получает ID, хэш пароля и роли для проверки входа"""
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            request = user_profile_pb2.GetUserAuthRequest(email=email)
            
            try:
                resp = await stub.GetUserAuthData(request)
                
                roles_mapped = [user_profile_pb2.UserRole.Name(r) for r in resp.roles]
                return UserAuthData(
                    user_id=resp.user_id,
                    password_hash=resp.password_hash,
                    roles=roles_mapped
                )
            except grpc.RpcError as e:
                return None

    def _map_proto_to_pydantic(self, proto_user) -> UserProfileResponse:
        last_donation_dt = None
        if proto_user.last_donation_at and proto_user.last_donation_at.seconds > 0:
            last_donation_dt = proto_user.last_donation_at.ToDatetime()
        last_donation_date = last_donation_dt.date() if last_donation_dt else None

        roles_mapped = [UserRole(user_profile_pb2.UserRole.Name(r)) for r in proto_user.roles]
        lives_saved = getattr(proto_user, "lives_saved_count", None)
        if lives_saved is None:
            lives_saved = proto_user.total_donations * 3

        name = getattr(proto_user, "name", None) or getattr(proto_user, "full_name", None) or ""

        return UserProfileResponse(
            id=proto_user.user_id,
            name=name,
            email=proto_user.email or "",
            phone=getattr(proto_user, "phone", None) or None,
            avatar=getattr(proto_user, "avatar_url", None) or None,
            last_donation=last_donation_date,
            total_donations=proto_user.total_donations,
            blood_type=proto_user.blood_type or "N/A",
            lives_saved_count=lives_saved,
            donor_status=getattr(proto_user, "donor_status", None) or "",
            has_donor_book=getattr(proto_user, "has_donor_book", False),
            test_is_done=getattr(proto_user, "test_is_done", False),
            birth_date=_birth_date_from_proto(proto_user),
            roles=roles_mapped,
            is_active=proto_user.is_active,
            is_banned=proto_user.is_banned,
            is_verified=proto_user.is_verified,
        )