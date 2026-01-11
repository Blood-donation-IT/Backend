from functools import lru_cache
from src.config import settings
from src.infrastructure.grpc.user_client import UserGrpcClient

@lru_cache()
def get_user_grpc_client() -> UserGrpcClient:
    print("🔌 Establishing connection to User gRPC Service...")
    return UserGrpcClient(
        host=settings.USER_SERVICE_HOST,
        port=settings.USER_SERVICE_PORT
    )