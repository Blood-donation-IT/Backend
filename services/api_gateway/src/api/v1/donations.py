from datetime import date, datetime
from typing import Annotated, Optional

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
    DonationAnalyticsResponse,
    DonationAnalyticsSlot,
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


@router.get("/donations/analytics", response_model=DonationAnalyticsResponse) # аналітика записів на обрану локацію та день 
async def get_donations_analytics(
    _user_id: Annotated[int, Depends(get_current_user_id)],
    application_day: Optional[date] = Query(None, alias="applicationDay"),
    application_day_snake: Optional[date] = Query(None, alias="application_day"),
    location_id: Optional[str] = Query(None),
    location_id_camel: Optional[str] = Query(None, alias="locationId"),
    slot_index: Optional[int] = Query(None, ge=0, le=10),
    slot_index_camel: Optional[int] = Query(
        None, ge=0, le=10, alias="slotIndex"
    ),
    client: ApplicationGrpcClient = Depends(get_application_grpc_client),
):
    day = application_day or application_day_snake
    if not day:
        raise HTTPException(
            status_code=400,
            detail="application_day is required",
        )
    selected_location_id = location_id or location_id_camel
    if not selected_location_id:
        raise HTTPException(
            status_code=400, detail="location_id is required",
        )
    try:
        date_dt = datetime.combine(day, datetime.min.time())
        data = await client.get_available_slots(date_dt, selected_location_id)
        slots_out = [
            DonationAnalyticsSlot(
                slot_index=s["slot_index"],
                time_label=s["time_label"],
                registered_count=s["booked_count"],
            )
            for s in data["slots"]
        ]
        by_idx = {s.slot_index: s.registered_count for s in slots_out}
        selected_slot = (
            slot_index if slot_index is not None else slot_index_camel
        )
        registered_selected = None
        if selected_slot is not None:
            if selected_slot not in by_idx:
                hi = max(by_idx) if by_idx else 0
                raise HTTPException(
                    status_code=400,
                    detail=f"slot_index must be between 0 and {hi}",
                )
            registered_selected = by_idx[selected_slot]

        return DonationAnalyticsResponse(
            location_id=selected_location_id,
            application_day=day.isoformat(),
            total_registered=data["daily_booked"],
            slots=slots_out,
            selected_slot_index=selected_slot,
            registered_for_selected_slot=registered_selected,
        )
    except grpc.RpcError as e:
        raise _map_grpc_error(e) from e
    except HTTPException:
        raise
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
