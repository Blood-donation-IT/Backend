from fastapi import APIRouter, HTTPException, Depends
from src.schemas.donations import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    GetApplicationsResponse,
    ApplicationResponse,
    CancelApplicationResponse
)
from src.infrastructure.grpc.application_client import ApplicationGrpcClient
from src.config import settings

router = APIRouter(tags=["Donations"])


def get_application_client() -> ApplicationGrpcClient:
    return ApplicationGrpcClient(
        host=settings.APPLICATION_MANAGEMENT_SERVICE_HOST,
        port=settings.APPLICATION_MANAGEMENT_SERVICE_PORT
    )


@router.get("/donations/get_applications", response_model=GetApplicationsResponse)
async def get_applications(user_id: int, client: ApplicationGrpcClient = Depends(get_application_client)):
    try:
        applications_data = await client.get_applications_by_user(user_id)
        applications = [
            ApplicationResponse(**app) for app in applications_data
        ]
        return GetApplicationsResponse(applications=applications)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/donations/create_application", response_model=CreateApplicationResponse)
async def create_application(
    request: CreateApplicationRequest,
    client: ApplicationGrpcClient = Depends(get_application_client)
):
    try:
        result = await client.create_application(request)
        return CreateApplicationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/donations/{application_id}/cancel", response_model=CancelApplicationResponse)
async def cancel_application(
    application_id: int,
    client: ApplicationGrpcClient = Depends(get_application_client)
):
    try:
        result = await client.cancel_application(application_id)
        return CancelApplicationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
