import asyncio
import grpc
import sys

from src.container import Container
from contracts.authorization import authorization_pb2_grpc

async def serve(container: Container) -> None:
    server = grpc.aio.server()
    authorization_service_instance = await container.authorization_service()
    
    authorization_pb2_grpc.add_AuthorizationServiceServicer_to_server(
        authorization_service_instance,
        server
    )
    
    server.add_insecure_port("[::]:50053")
    await server.start()
    print("Async gRPC server started on port 50053 (with DI Container)", file=sys.stderr)
    await server.wait_for_termination()

async def main() -> None:
    container = Container()
    
    container.config.repository_type.from_env("REPOSITORY_TYPE", "postgresql")
    container.config.id_generator_type.from_env("ID_GENERATOR_TYPE", "snowflake")
    
    container.wire(modules=[__name__])
    
    await container.init_resources()
    
    from src.infrastructure.db.base import on_startup
    await on_startup()
    
    try:
        await serve(container)
    except KeyboardInterrupt:
        print("Shutting down gRPC server...", file=sys.stderr)
    finally:
        await container.shutdown_resources()
        print("Container resources shut down gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)









