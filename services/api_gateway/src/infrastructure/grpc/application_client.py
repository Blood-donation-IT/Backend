import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from contracts.application_management import application_management_pb2, application_management_pb2_grpc
from datetime import datetime
from typing import List, Optional
from src.schemas.donations import ApplicationResponse, CreateApplicationRequest


class ApplicationGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def create_application(self, user_id: int, request: CreateApplicationRequest) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            
            ts_time = Timestamp()
            ts_time.FromDatetime(request.application_time)
            
            ts_day = None
            if request.application_day:
                ts_day = Timestamp()
                ts_day.FromDatetime(request.application_day)
            
            grpc_request = application_management_pb2.CreateApplicationRequest(
                user_id=user_id,
                blood_type=request.blood_type,
                application_time=ts_time,
                application_day=ts_day if ts_day else None,
                location_id=request.location_id or "",
                status=request.status or "pending"
            )
            
            try:
                response = await stub.CreateApplication(grpc_request)
                return {
                    "application_id": response.application_id,
                    "success": response.success,
                    "message": response.message
                }
            except grpc.RpcError:
                raise

    async def get_applications_by_user(self, user_id: int) -> List[dict]:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            
            request = application_management_pb2.GetApplicationRequest(user_id=user_id)
            
            try:
                applications = []
                async for proto_app in stub.GetApplicationByUser(request):
                    app_dict = {
                        "application_id": proto_app.application_id,
                        "user_id": proto_app.user_id,
                        "blood_type": proto_app.blood_type,
                        "application_time": proto_app.application_time.ToDatetime() if proto_app.HasField("application_time") else None,
                        "application_day": proto_app.application_day.ToDatetime() if proto_app.HasField("application_day") else None,
                        "location_id": proto_app.location_id if proto_app.location_id else None,
                        "status": proto_app.status,
                        "created_at": proto_app.created_at.ToDatetime() if proto_app.HasField("created_at") else None,
                        "updated_at": proto_app.updated_at.ToDatetime() if proto_app.HasField("updated_at") else None
                    }
                    applications.append(app_dict)
                return applications
            except grpc.RpcError:
                raise

    async def cancel_application(self, application_id: int, user_id: int) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            
            request = application_management_pb2.ApplicationRequest(
                application_id=application_id, user_id=user_id
            )
            
            try:
                response = await stub.CancelApplication(request)
                return {
                    "application_id": response.application_id,
                    "success": response.success,
                    "message": response.message
                }
            except grpc.RpcError:
                raise
