import asyncio
import grpc
import sys

from src.container import Container
from contracts.application_management import application_management_pb2_grpc

async def serve(container: Container) -> None:
    server = grpc.aio.server()
    application_management_service_instance = await container.application_management_service()
    
    application_management_pb2_grpc.add_ApplicationManagementServiceServicer_to_server(
        application_management_service_instance,
        server
    )
    
    server.add_insecure_port("[::]:50052")
    await server.start()
    print("Async gRPC server started on port 50052 (with DI Container)", file=sys.stderr)
    await server.wait_for_termination()

async def main() -> None:
    from src.infrastructure.db.base import on_startup
    await on_startup()
    
    container = Container()
    
    container.config.repository_type.from_env("REPOSITORY_TYPE", "postgresql")
    container.config.id_generator_type.from_env("ID_GENERATOR_TYPE", "snowflake")
    
    container.wire(modules=[__name__])
    
    await container.init_resources()
    try:
        await serve(container)
    except KeyboardInterrupt:
        print("Shutting down gRPC server", file=sys.stderr)
    finally:
        await container.shutdown_resources()
        print("Container resources shut down gracefully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)