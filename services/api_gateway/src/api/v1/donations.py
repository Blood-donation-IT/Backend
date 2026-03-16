from datetime import date, datetime
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.donations import (
    CreateApplicationRequest,
    CreateApplicationResponse,
    GetApplicationsResponse,
    ApplicationResponse,
    CancelApplicationResponse,
    GetAvailableSlotsResponse,
    GetCalendarAvailabilityResponse,
)
from src.infrastructure.grpc.application_client import ApplicationGrpcClient
from src.api.dependencies import get_application_grpc_client

router = APIRouter(tags=["Donations"])


@router.get("/donations/available_slots", response_model=GetAvailableSlotsResponse)
async def get_available_slots(
    date: date,
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    try:
        date_dt = datetime.combine(date, datetime.min.time())
        result = await client.get_available_slots(date_dt)
        return GetAvailableSlotsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/donations/calendar_availability", response_model=GetCalendarAvailabilityResponse)
async def get_calendar_availability(
    year: int,
    month: int,
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="month must be 1–12")
    try:
        result = await client.get_calendar_availability(year, month)
        return GetCalendarAvailabilityResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
    "/donations/{application_id}/cancel",
    response_model=CancelApplicationResponse,
)
async def cancel_application(
    application_id: str,
    client: ApplicationGrpcClient = Depends(get_application_grpc_client)
):
    try:
        aid = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application_id")
    try:
        result = await client.cancel_application(aid)
        return CancelApplicationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
