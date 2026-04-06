import asyncio
import grpc
import sys

from contracts.notifications import notifications_pb2_grpc
from src.container import Container


async def serve(container: Container) -> None:
    server = grpc.aio.server()
    service = await container.notifications_service()
    notifications_pb2_grpc.add_NotificationsServiceServicer_to_server(service, server)
    server.add_insecure_port("[::]:50054")
    await server.start()
    print("Notifications gRPC server started on port 50054", file=sys.stderr)
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
        print("Notifications server shutdown requested", file=sys.stderr)
    finally:
        await container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
