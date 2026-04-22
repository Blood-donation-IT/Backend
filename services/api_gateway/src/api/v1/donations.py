from datetime import date, datetime
from typing import Annotated

import grpc
from fastapi import APIRouter, HTTPException, Depends, Query

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
from src.core.auth import get_current_user_id

router = APIRouter(tags=["Donations"])


def _map_grpc_error(e: grpc.RpcError) -> HTTPException:
    code = e.code()
    detail = e.details() or "gRPC error"
    if code == grpc.StatusCode.PERMISSION_DENIED:
        return HTTPException(status_code=403, detail=detail)
    if code == grpc.StatusCode.NOT_FOUND:
        return HTTPException(status_code=404, detail=detail)
    if code == grpc.StatusCode.INVALID_ARGUMENT:
        return HTTPException(status_code=400, detail=detail)
    if code == grpc.StatusCode.UNAVAILABLE:
        return HTTPException(
            status_code=503,
            detail=(
                f"{detail}. Verify APPLICATION_MANAGEMENT_SERVICE_HOST and "
                "APPLICATION_MANAGEMENT_SERVICE_PORT variables."
            ),
        )
    return HTTPException(status_code=502, detail=detail)


@router.get("/donations/available_slots", response_model=GetAvailableSlotsResponse)
async def get_available_slots(
    _user_id: Annotated[int, Depends(get_current_user_id)],
    date: date,
    location_id: str | None = Query(None),
    location_id_camel: str | None = Query(None, alias="locationId"),
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    selected_location_id = location_id or location_id_camel
    if not selected_location_id:
        raise HTTPException(
            status_code=400, detail="location_id (or locationId) is required"
        )
    try:
        date_dt = datetime.combine(date, datetime.min.time())
        result = await client.get_available_slots(date_dt, selected_location_id)
        return GetAvailableSlotsResponse(**result)
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/donations/calendar_availability", response_model=GetCalendarAvailabilityResponse)
async def get_calendar_availability(
    _user_id: Annotated[int, Depends(get_current_user_id)],
    year: int,
    month: int,
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="month must be 1–12")
    try:
        result = await client.get_calendar_availability(year, month)
        return GetCalendarAvailabilityResponse(**result)
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/donations/get_applications", response_model=GetApplicationsResponse)
async def get_applications(
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    try:
        applications_data = await client.get_applications_by_user(user_id)
        applications = [
            ApplicationResponse(**app) for app in applications_data
        ]
        return GetApplicationsResponse(applications=applications)
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/donations/create_application", response_model=CreateApplicationResponse)
async def create_application(
    request: CreateApplicationRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    try:
        result = await client.create_application(user_id, request)
        return CreateApplicationResponse(**result)
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/donations/{application_id}/cancel",
    response_model=CancelApplicationResponse,
)
async def cancel_application(
    application_id: str,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    try:
        aid = int(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application_id")
    try:
        result = await client.cancel_application(aid, user_id)
        return CancelApplicationResponse(**result)
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
