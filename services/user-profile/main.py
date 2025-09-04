import asyncio
import grpc


from src.infrastructure.grpc.user_profile_server import UserProfileService
from contracts.user import user_profile_pb2_grpc
from src.infrastructure.repositories.sqlalchemy_user_repository import SQlAlchemyUserRepository
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.application.use_cases.create_user import CreateUserUseCase
from src.infrastructure.repositories.factory import get_user_repo

# from src.application.use_cases.get_user_by_id import GetUserByIdUseCase



async def serve()->None:
    
    server:grpc.aio.Server = grpc.aio.server()
    async with get_user_repo() as repo:       
        id_gen:SnowflakeIDGenerator = SnowflakeIDGenerator(
            instance=1
        )
        #TODO: Create Python dependency injection container :\
        create_user_profile_use_case:CreateUserUseCase = CreateUserUseCase(
            repository=repo,
            id_generator=id_gen
            )
        user_profile_service = UserProfileService(
        create_user_profile_use_case=create_user_profile_use_case,
        # get_user_by_id_use_case=,
        )
        user_profile_pb2_grpc.add_UserProfileServiceServicer_to_server(
            user_profile_service,
            server
            )

        server.add_insecure_port("[::]:50051")
        await server.start()
        print(" Async gRPC server started on port 50051")

        await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())