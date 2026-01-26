import grpc
from contracts.application_management import application_management_pb2, application_management_pb2_grpc
from src.application.use_cases.create_application import CreateApplicationUseCase
from src.application.use_cases.update_application import UpdateApplicationUseCase
from src.application.use_cases.get_application import GetApplicationUseCase
from src.domain.entities.application import Application 
from google.protobuf.timestamp_pb2 import Timestamp


class ApplicationManagementService(application_management_pb2_grpc.ApplicationManagementServiceServicer):
    def __init__(self, create_use_case, update_use_case, get_use_case, repository=None):
        self.create_use_case = create_use_case
        self.update_use_case = update_use_case
        self.get_use_case = get_use_case
        self.repository = repository

    async def CreateApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            import datetime
            
            if not request.HasField("application_time"):
                context.set_details("application_time is required")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return application_management_pb2.ApplicationResponse(success=False, message="application_time is required")
            
            application_time_dt = request.application_time.ToDatetime()
            
            application_day_dt = None
            if request.HasField("application_day"):
                application_day_dt = request.application_day.ToDatetime()
            
            application = await self.create_use_case.execute(
                user_id=request.user_id,
                blood_type=request.blood_type,
                application_time=application_time_dt,
                application_day=application_day_dt,
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
                
                yield application_management_pb2.Application(
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
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

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
