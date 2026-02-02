import asyncio
import grpc
from contracts.user import user_profile_pb2_grpc, user_profile_pb2

class UserProfileClient:
    def __init__(self, host="user-profile", port=50051):
        self.target = f"{host}:{port}"

    async def create_profile(self, name, email, phone):
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = user_profile_pb2_grpc.UserProfileServiceStub(channel)
            req = user_profile_pb2.CreateProfileRequest(
                name=name,
                email=email,
                phone=phone
            )
            resp = await stub.CreateProfile(req)
            return resp