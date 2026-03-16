import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from contracts.application_management import application_management_pb2, application_management_pb2_grpc
from datetime import datetime
from typing import List, Optional
from src.schemas.donations import ApplicationResponse, CreateApplicationRequest


class ApplicationGrpcClient:
    def __init__(self, host: str, port: int):
        self.target = f"{host}:{port}"

    async def create_application(self, request: CreateApplicationRequest) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)

            ts_day = Timestamp()
            ts_day.FromDatetime(request.application_day)

            grpc_request = application_management_pb2.CreateApplicationRequest(
                user_id=request.user_id,
                blood_type=request.blood_type,
                application_day=ts_day,
                slot_index=request.slot_index,
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
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in create_application: {e.details()}")

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
                        "slot_index": getattr(proto_app, "slot_index", None),
                        "location_id": proto_app.location_id if proto_app.location_id else None,
                        "status": proto_app.status,
                        "created_at": proto_app.created_at.ToDatetime() if proto_app.HasField("created_at") else None,
                        "updated_at": proto_app.updated_at.ToDatetime() if proto_app.HasField("updated_at") else None
                    }
                    applications.append(app_dict)
                return applications
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in get_applications_by_user: {e.details()}")

    async def cancel_application(self, application_id: int) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            
            request = application_management_pb2.ApplicationRequest(application_id=application_id)
            
            try:
                response = await stub.CancelApplication(request)
                return {
                    "application_id": response.application_id,
                    "success": response.success,
                    "message": response.message
                }
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in cancel_application: {e.details()}")

    async def get_available_slots(self, date: datetime) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            ts = Timestamp()
            ts.FromDatetime(date)
            request = application_management_pb2.GetAvailableSlotsRequest(date=ts)
            try:
                response = await stub.GetAvailableSlots(request)
                out = {
                    "slots": [
                        {
                            "slot_index": s.slot_index,
                            "time_label": s.time_label,
                            "booked_count": s.booked_count,
                            "capacity": s.capacity,
                            "is_available": s.is_available,
                        }
                        for s in response.slots
                    ],
                    "daily_booked": response.daily_booked,
                    "daily_capacity": response.daily_capacity,
                }
                if hasattr(response, "day_available"):
                    out["day_available"] = response.day_available
                if hasattr(response, "reason"):
                    out["reason"] = response.reason or ""
                return out
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in get_available_slots: {e.details()}")

    async def get_calendar_availability(self, year: int, month: int) -> dict:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = application_management_pb2_grpc.ApplicationManagementServiceStub(channel)
            request = application_management_pb2.GetCalendarAvailabilityRequest(
                year=year, month=month
            )
            try:
                response = await stub.GetCalendarAvailability(request)
                return {"available_dates": list(response.available_dates)}
            except grpc.RpcError as e:
                raise Exception(f"gRPC Error in get_calendar_availability: {e.details()}")
