import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from contracts.authorization import authorization_pb2, authorization_pb2_grpc
from datetime import datetime
from typing import Optional


class AuthorizationGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def register(self, email: str, password: str, confirm_password: str, name: str) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = authorization_pb2_grpc.AuthorizationServiceStub(channel)
            
            request = authorization_pb2.RegisterRequest(
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password
            )
            
            try:
                response = await stub.Register(request)
                return {
                    "success": response.success,
                    "message": response.message,
                    "user_id": response.user_id,
                    "email": response.email
                }
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in register: {e.details()}")

    async def login(self, email: str, password: str) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = authorization_pb2_grpc.AuthorizationServiceStub(channel)
            
            request = authorization_pb2.LoginRequest(
                email=email,
                password=password
            )
            
            try:
                response = await stub.Login(request)
                expires_at = None
                if response.HasField("expires_at"):
                    expires_at = response.expires_at.ToDatetime()
                
                return {
                    "success": response.success,
                    "message": response.message,
                    "access_token": response.access_token,
                    "refresh_token": response.refresh_token,
                    "user_id": response.user_id,
                    "email": response.email,
                    "expires_at": expires_at
                }
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in login: {e.details()}")

    async def refresh_token(self, refresh_token: str) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = authorization_pb2_grpc.AuthorizationServiceStub(channel)
            
            request = authorization_pb2.RefreshTokenRequest(
                refresh_token=refresh_token
            )
            
            try:
                response = await stub.RefreshToken(request)
                expires_at = None
                if response.HasField("expires_at"):
                    expires_at = response.expires_at.ToDatetime()
                
                return {
                    "success": response.success,
                    "message": response.message,
                    "access_token": response.access_token,
                    "refresh_token": response.refresh_token,
                    "expires_at": expires_at
                }
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in refresh_token: {e.details()}")
