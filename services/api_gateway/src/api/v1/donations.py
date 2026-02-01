from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.donations import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    GetApplicationsResponse,
    ApplicationResponse,
    CancelApplicationResponse
)
from src.infrastructure.grpc.application_client import ApplicationGrpcClient
from src.api.dependencies import get_application_grpc_client
from src.core.auth import get_current_user_id

router = APIRouter(tags=["Donations"])


@router.get("/donations/get_applications", response_model=GetApplicationsResponse)
async def get_applications(user_id: int, client: ApplicationGrpcClient = Depends(get_application_grpc_client)):
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
    client: ApplicationGrpcClient = Depends(get_application_grpc_client)
):
    try:
        result = await client.create_application(request)
        return CreateApplicationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/donations/cancel_my_application",
    response_model=CancelApplicationResponse,
)
async def cancel_my_application(
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    try:
        applications_data = await client.get_applications_by_user(user_id)
        active = [
            app for app in applications_data
            if app.get("status") in ("pending", "approved", "scheduled")
        ]
        if not active:
            raise HTTPException(
                status_code=404,
            )
        application_id = active[0]["application_id"]
        result = await client.cancel_application(application_id)
        return CancelApplicationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/donations/{application_id}/cancel",
    response_model=CancelApplicationResponse,
)
async def cancel_application(
    application_id: int,
    client: ApplicationGrpcClient = Depends(get_application_grpc_client)
):
    try:
        result = await client.cancel_application(application_id)
        return CancelApplicationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str)
