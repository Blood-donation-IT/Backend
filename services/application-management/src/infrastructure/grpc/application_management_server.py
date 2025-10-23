import grpc
from contracts.application_management import application_management_pb2, application_management_pb2_grpc
from src.application.use_cases.create_application import CreateApplicationUseCase
from src.application.use_cases.update_application import UpdateApplicationUseCase
from src.application.use_cases.get_application import GetApplicationUseCase
from src.domain.entities.application import Application 
from google.protobuf.timestamp_pb2 import Timestamp


class ApplicationManagementService(application_management_pb2_grpc.ApplicationManagementServiceServicer):
    def __init__(self, create_use_case, update_use_case, get_use_case):
        self.create_use_case = create_use_case
        self.update_use_case = update_use_case
        self.get_use_case = get_use_case

    async def CreateApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            application = await self.create_use_case.execute(
                user_id=request.user_id,
                blood_type=request.blood_type,
                application_time=request.application_time,
                description=request.description,
                status=request.status
            )
            return application_management_pb2.ApplicationResponse(
                application_id=application.id,
                success=True,
                message="Application created successfully"
            )
        except ValueError as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return application_management_pb2.ApplicationResponse(success=False, message=str(e))

    async def GetApplicationByUser(self, request, context: grpc.aio.ServicerContext):
        async for application in self.get_use_case.execute(request.user_id):
            ts = Timestamp()
            ts.FromDatetime(application.application_time)
            yield application_management_pb2.Application(
                application_id=application.id,
                user_id=application.user_id,
                blood_type=application.blood_type,
                application_time=ts,
                status=application.status,
                description=application.description,
                created_at=ts.FromDatetime(application.created_at),
                updated_at=ts.FromDatetime(application.updated_at)
            )

    async def UpdateApplication(self, request, context: grpc.aio.ServicerContext):
        try:
            application = await self.update_use_case.execute(
                application_id=request.application_id,
                application_time=request.application_time,
                description=request.description,
                blood_type=request.blood_type
            )
            return application_management_pb2.ApplicationResponse(
                application_id=application.id,
                success=True,
                message="Application updated successfully"
            )
        except ValueError as e:
            await context.set_details(str(e))
            await context.set_code(grpc.StatusCode.NOT_FOUND)
            return application_management_pb2.ApplicationResponse(success=False, message=str(e))
        
    