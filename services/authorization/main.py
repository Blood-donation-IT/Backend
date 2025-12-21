import asyncio
import grpc

from src.infrastructure.grpc.authorization_server import AuthorizationService
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.infrastructure.repositories.factory import get_authorization_repo
from contracts.authorization import authorization_pb2_grpc
from src.application.use_cases.register_use_case import RegisterUseCase
from src.application.use_cases.login_use_case import LoginUseCase
from src.application.use_cases.refresh_token_use_case import RefreshTokenUseCase

async def serve() -> None:
    server = grpc.aio.server()
    async with get_authorization_repo() as repo:
        id_gen = SnowflakeIDGenerator(instance=1) 
        register_use_case = RegisterUseCase(repository=repo, id_generator=id_gen)
        login_use_case = LoginUseCase(repository=repo)
        refresh_token_use_case = RefreshTokenUseCase(repository=repo)

        authorization_service = AuthorizationService(
            register_use_case=register_use_case,
            login_use_case=login_use_case,
            refresh_token_use_case=refresh_token_use_case
        )

        authorization_pb2_grpc.add_AuthorizationServiceServicer_to_server(authorization_service, server)
        server.add_insecure_port("[::]:50053")
        print("Async gRPC server started on port 50053")
        await server.start()
        await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())








