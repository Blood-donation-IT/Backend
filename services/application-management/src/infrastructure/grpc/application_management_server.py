import grpc
from contracts.application_management import application_management_pb2, application_management_pb2_grpc
from src.application.use_cases.create_application import CreateApplicationUseCase
from src.application.use_cases.update_application import UpdateApplicationUseCase
from src.application.use_cases.get_application import GetApplicationUseCase
from src.domain.entities.application import Application 
from google.protobuf.timestamp_pb2 import Timestamp


class ApplicationManagementService(application_management_pb2_grpc.ApplicationManagementServiceServicer):
    def __init__(self, create_use_case, update_use_case, get_use_case, get_available_slots_use_case=None, get_calendar_availability_use_case=None, repository=None):
        self.create_use_case = create_use_case
        self.update_use_case = update_use_case
        self.get_use_case = get_use_case
        self.get_available_slots_use_case = get_available_slots_use_case
        self.get_calendar_availability_use_case = get_calendar_availability_use_case
        self.repository = repository

    async def CreateApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            import datetime

            if request.user_id <= 0:
                context.set_details("user_id is required and must be positive")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.ApplicationResponse(
                    success=False, message="Invalid user_id"
                )

            if not request.HasField("application_time"):
                context.set_details("application_time is required")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.ApplicationResponse(success=False, message="application_day is required")

            application_day_dt = request.application_day.ToDatetime()
            slot_index = getattr(request, "slot_index", 0)
            if not (0 <= slot_index <= 9):
                context.set_details("slot_index must be 0–9")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.ApplicationResponse(success=False, message="slot_index must be 0–9")

            application = await self.create_use_case.execute(
                user_id=request.user_id,
                blood_type=request.blood_type,
                application_day=application_day_dt,
                slot_index=slot_index,
                location_id=request.location_id if request.location_id else None,
                status=request.status if request.status else "pending"
            )
            return application_management_pb2.ApplicationResponse(
                application_id=application.id,
                success=True,
                message="Application created successfully"
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return application_management_pb2.ApplicationResponse(success=False, message=str(e))
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return application_management_pb2.ApplicationResponse(success=False, message=f"Internal server error: {str(e)}")

    async def GetApplicationByUser(self, request, context: grpc.aio.ServicerContext):
        try:
            if request.user_id <= 0:
                context.set_details("user_id is required and must be positive")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return

            async for application in self.get_use_case.execute(request.user_id):
                ts_time = Timestamp()
                ts_time.FromDatetime(application.application_time)
                
                ts_day = Timestamp()
                if application.application_day:
                    ts_day.FromDatetime(application.application_day)
                
                ts_created = Timestamp()
                if application.created_at:
                    ts_created.FromDatetime(application.created_at)
                
                ts_updated = Timestamp()
                if application.updated_at:
                    ts_updated.FromDatetime(application.updated_at)
                
                app_msg = application_management_pb2.Application(
                    application_id=application.id,
                    user_id=application.user_id,
                    blood_type=application.blood_type,
                    application_time=ts_time,
                    application_day=ts_day if application.application_day else None,
                    location_id=application.location_id if application.location_id else "",
                    status=application.status,
                    created_at=ts_created if application.created_at else None,
                    updated_at=ts_updated if application.updated_at else None
                )
                if hasattr(app_msg, "slot_index") and getattr(application, "slot_index", None) is not None:
                    app_msg.slot_index = application.slot_index
                yield app_msg
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

    async def GetAvailableSlots(self, request, context: grpc.aio.ServicerContext):
        try:
            if not request.HasField("date"):
                context.set_details("date is required")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.GetAvailableSlotsResponse()
            date_dt = request.date.ToDatetime()
            data = await self.get_available_slots_use_case.execute(date_dt)
            slot_infos = [
                application_management_pb2.SlotInfo(
                    slot_index=s["slot_index"],
                    time_label=s["time_label"],
                    booked_count=s["booked_count"],
                    capacity=s["capacity"],
                    is_available=s["is_available"],
                )
                for s in data["slots"]
            ]
            resp = application_management_pb2.GetAvailableSlotsResponse(
                slots=slot_infos,
                daily_booked=data["daily_booked"],
                daily_capacity=data["daily_capacity"],
            )
            if hasattr(resp, "day_available"):
                resp.day_available = data.get("day_available", True)
            if hasattr(resp, "reason"):
                resp.reason = data.get("reason", "")
            return resp
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return application_management_pb2.GetAvailableSlotsResponse()

    async def GetCalendarAvailability(self, request, context: grpc.aio.ServicerContext):
        try:
            year = getattr(request, "year", None) or 0
            month = getattr(request, "month", None) or 0
            if not (1 <= month <= 12) or year < 2000:
                context.set_details("year and month (1–12) required")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.GetCalendarAvailabilityResponse()
            dates = await self.get_calendar_availability_use_case.execute(year, month)
            return application_management_pb2.GetCalendarAvailabilityResponse(
                available_dates=dates
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return application_management_pb2.GetCalendarAvailabilityResponse()

    async def UpdateApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            import datetime
            application_time_dt = None
            if request.HasField("application_time"):
                application_time_dt = request.application_time.ToDatetime()
            
            application = await self.update_use_case.execute(
                application_id=request.application_id,
                application_time=application_time_dt,
                description=request.description if hasattr(request, 'description') else None,
                blood_type=request.blood_type if hasattr(request, 'blood_type') else None
            )
            return application_management_pb2.ApplicationResponse(
                application_id=application.id,
                success=True,
                message="Application updated successfully"
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return application_management_pb2.ApplicationResponse(success=False, message=str(e))
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return application_management_pb2.ApplicationResponse(success=False, message=f"Internal server error: {str(e)}")

    async def CancelApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            if request.user_id <= 0:
                context.set_details("user_id is required and must be positive")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.ApplicationResponse(
                    success=False, message="Invalid user_id"
                )

            existing = await self.repository.get_by_id(request.application_id)
            if not existing:
                context.set_details(f"Application with id {request.application_id} not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return application_management_pb2.ApplicationResponse(
                    success=False, message="Application not found"
                )
            if existing.user_id != request.user_id:
                context.set_details("Permission denied")
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return application_management_pb2.ApplicationResponse(
                    success=False, message="Permission denied"
                )

            application = await self.update_use_case.execute(
                application_id=request.application_id,
                status="cancelled"
            )
            
            return application_management_pb2.ApplicationResponse(
                application_id=application.id,
                success=True,
                message="Application cancelled successfully"
            )
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return application_management_pb2.ApplicationResponse(success=False, message=str(e))
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return application_management_pb2.ApplicationResponse(success=False, message=f"Internal server error: {str(e)}")
