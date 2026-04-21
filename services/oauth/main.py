import asyncio
import grpc
import sys
import requests

from contracts.oauth import oauth_pb2_grpc
from src.oauth_server import OAuthService


async def serve() -> None:
    server = grpc.aio.server()
    oauth_pb2_grpc.add_OAuthServiceServicer_to_server(OAuthService(), server)
    server.add_insecure_port("[::]:50055")
    await server.start()
    print("OAuth gRPC server started on port 50055", file=sys.stderr)
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
