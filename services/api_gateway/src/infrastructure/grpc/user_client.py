import grpc
from google.protobuf.timestamp_pb2 import Timestamp
# Импорты твоих контрактов
from contracts.user import user_profile_pb2, user_profile_pb2_grpc
from src.schemas.user import UserProfileResponse, UserRole
from typing import Optional

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
                return self._map_proto_to_pydantic(proto_user)
            except grpc.RpcError as e:
                print(f"GRPC Error in get_profile: {e}")
                raise e

    # --- ВОТ ЭТОГО НЕ ХВАТАЛО ---
    async def create_user(self, email: str, full_name: str, password_hash: str, phone: str = None) -> UserProfileResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            
            # Собираем запрос для gRPC
            # ВАЖНО: Убедись, что в .proto ты добавил поле password_hash!
            request = user_profile_pb2.CreateProfileRequest(
                email=email,
                full_name=full_name,
                password_hash=password_hash, # <-- Мы передаем хэш
                phone=phone or ""
            )
            
            try:
                # Вызываем метод CreateProfile (как в .proto файле)
                proto_user = await stub.CreateProfile(request)
                return self._map_proto_to_pydantic(proto_user)
            except grpc.RpcError as e:
                print(f"GRPC Error in create_user: {e}")
                # Тут можно добавить проверку e.code() == grpc.StatusCode.ALREADY_EXISTS
                raise Exception(f"Failed to create user: {e.details()}")

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
        if proto_user.last_donation_at.seconds > 0:
            last_donation_dt = proto_user.last_donation_at.ToDatetime()

        roles_mapped = [UserRole(user_profile_pb2.UserRole.Name(r)) for r in proto_user.roles]
        lives_saved = proto_user.total_donations * 3

        return UserProfileResponse(
            id=proto_user.user_id,
            full_name=proto_user.full_name,
            email=proto_user.email,
            phone=None, 
            blood_type=proto_user.blood_type,
            total_donations=proto_user.total_donations,
            last_donation_at=last_donation_dt,
            lives_saved_count=lives_saved,
            roles=roles_mapped,
            is_active=proto_user.is_active,
            is_verified=proto_user.is_verified,
        )