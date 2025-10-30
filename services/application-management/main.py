import asyncio
import grpc

from src.infrastructure.grpc.application_management_server import ApplicationManagementService
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.infrastructure.repositories.sqlalchemy_application_repository import SQlAlchemyUserRepository
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.infrastructure.repositories.factory import get_application_repo
from contracts.application_management import application_management_pb2_grpc
from src.application.use_cases.create_application import CreateApplicationUseCase
from src.application.use_cases.update_application import UpdateApplicationUseCase
from src.application.use_cases.get_application import GetApplicationUseCase

async def serve() -> None:
    server = grpc.aio.server()
    async with get_application_repo() as repo:
        id_gen = SnowflakeIDGenerator(instance=2)  
        create_use_case = CreateApplicationUseCase(repository=repo, id_generator=id_gen)
        update_use_case = UpdateApplicationUseCase(repository=repo)
        get_use_case = GetApplicationUseCase(repository=repo)

        application_management_service = ApplicationManagementService(
            create_use_case=create_use_case,
            update_use_case=update_use_case,
            get_use_case=get_use_case
        )

        application_management_pb2_grpc.add_ApplicationManagementServiceServicer_to_server(application_management_service, server)
        server.add_insecure_port("[::]:50052")  
        print("Async gRPC server started on port 50052")
        await server.start()
        await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())