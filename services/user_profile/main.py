import asyncio
import grpc


from src.infrastructure.grpc.user_profile_server import UserProfileService
from contracts.user import user_profile_pb2_grpc
from src.infrastructure.repositories.sqlalchemy_user_repository import SQlAlchemyUserRepository
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.application.use_cases.create_user import CreateUserUseCase
from src.infrastructure.repositories.factory import get_user_repo
from src.container import Container
# from grpc_health.v1 import health, health_pb2_grpc,health_pb2
# from src.application.use_cases.get_user_by_id import GetUserByIdUseCase
import sys



async def serve(container: Container)->None:
    
    server:grpc.aio.Server = grpc.aio.server()
    user_profile_instance:UserProfileService = await container.user_profile_service()
    user_profile_pb2_grpc.add_UserProfileServiceServicer_to_server(
        user_profile_instance,
        server
    )
    #TODO: Implement health check service 
    
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Async gRPC server started on port 50051 (with DI Container)",file=sys.stderr)
    await server.wait_for_termination()

async def main()->None:
    container:Container = Container()
    
    container.config.repository_type.from_env("REPOSITORY_TYPE", "postgresql")
    container.config.id_generator_type.from_env("ID_GENERATOR_TYPE", "snowflake")
    
    container.wire(modules=[__name__])
    
    await container.init_resources()  
    try:
        await serve(container)
    except KeyboardInterrupt:
        print("Shutting down gRPC server...",file=sys.stderr)
    finally:
        await container.shutdown_resources()
        print("Container resources shut down gracefully.")
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user",file=sys.stderr)
    