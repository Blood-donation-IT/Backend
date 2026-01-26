from functools import lru_cache
from src.config import settings
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.infrastructure.grpc.authorization_client import AuthorizationGrpcClient
from src.infrastructure.grpc.application_client import ApplicationGrpcClient

@lru_cache()
def get_user_grpc_client() -> UserGrpcClient:
    print("🔌 Establishing connection to User gRPC Service...")
    return UserGrpcClient(
        host=settings.USER_SERVICE_HOST,
        port=settings.USER_SERVICE_PORT
    )

@lru_cache()
def get_authorization_grpc_client() -> AuthorizationGrpcClient:
    print("Establishing connection to Authorization gRPC Service...")
    return AuthorizationGrpcClient(
        host=settings.AUTHORIZATION_SERVICE_HOST,
        port=settings.AUTHORIZATION_SERVICE_PORT
    )

@lru_cache()
def get_application_grpc_client() -> ApplicationGrpcClient:
    print("Establishing connection to Application Management gRPC Service...")
    return ApplicationGrpcClient(
        host=settings.APPLICATION_MANAGEMENT_SERVICE_HOST,
        port=settings.APPLICATION_MANAGEMENT_SERVICE_PORT
    )