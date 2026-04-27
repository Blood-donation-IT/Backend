from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.application import Application
from src.domain.constants import (
    SLOT_CAPACITY,
    DAILY_CAPACITY,
    NUM_SLOTS,
    LOCATIONS,
    SLOT_TIME_LABELS
)
from src.domain.booking_rules import get_day_availability_reason

import datetime
from typing import Optional


def _slot_index_to_time(slot_index: int) -> tuple[int, int]:
    if not 0 <= slot_index < NUM_SLOTS:
        raise ValueError(f"slot_index must be 0–9, got {slot_index}")
    hour = 8 + (slot_index // 2)
    minute = (slot_index % 2) * 30
    return hour, minute


def _application_day_to_date(application_day: datetime.datetime) -> datetime.date:
    if hasattr(application_day, "date"):
        return application_day.date()
    return application_day


class CreateApplicationUseCase:
    def __init__(self, repository: IApplicationRepository, id_generator: IIDGenerator):
        self.application_repository: IApplicationRepository = repository
        self.id_generator: IIDGenerator = id_generator

    async def execute(self,
                      user_id: int,
                      blood_type: str,
                      application_day: datetime.datetime,
                      slot_index: int,
                      application_time: Optional[datetime.datetime] = None,
                      location_id: Optional[str] = None,
                      status: str = "pending",
                      description: Optional[str] = None,
                      created_at: Optional[datetime.datetime] = None,
                      updated_at: Optional[datetime.datetime] = None) -> Application:
        if not 0 <= slot_index < NUM_SLOTS:
            raise ValueError(f"slot_index must be 0–9, got {slot_index}")
        if not location_id:
            raise ValueError("location_id is required")
        if location_id not in LOCATIONS:
            raise ValueError(
                f"location_id must be one of: {', '.join(LOCATIONS)}"
            )
        if not application_time:
            raise ValueError("Either application_time must be provided")
        if application_time not in SLOT_TIME_LABELS:
            raise ValueError(
                f"application_time must be one of: {', '.join(SLOT_TIME_LABELS)}"
            )
        date_only = _application_day_to_date(application_day)

        reason = get_day_availability_reason(date_only)
        if reason == "past":
            raise ValueError("Cannot book in the past")
        if reason == "weekend":
            raise ValueError("Booking on weekends is not available")
        if reason == "out_of_range":
            raise ValueError("Booking is allowed only up to 2 months ahead")

        # перевірка чи вже є активна заявка для цього user_id
        async for existing_app in self.application_repository.find_by_user_id(user_id):
            if existing_app.status in ["pending", "approved", "scheduled"]:
                raise ValueError(
                    f"User {user_id} already has an active application "
                    f"(id: {existing_app.id}, status: {existing_app.status})"
                )

       
        booked_in_slot = await self.application_repository.count_booked_by_date_and_slot(
            date_only, slot_index, location_id
        )
        if booked_in_slot >= SLOT_CAPACITY:
            raise ValueError(
                f"Slot {slot_index} on {date_only} is full ({SLOT_CAPACITY} people max)"
            )

        booked_in_day = await self.application_repository.count_booked_by_date(
            date_only, location_id
        )
        if booked_in_day >= DAILY_CAPACITY:
            raise ValueError(f"Day {date_only} is full ({DAILY_CAPACITY} people max)")

        if application_time is None:
            hour, minute = _slot_index_to_time(slot_index)
            application_time = application_day.replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )

        day_dt = datetime.datetime.combine(
            date_only, datetime.time(0, 0, 0), tzinfo=getattr(application_day, "tzinfo", None)
        )

        application_id: int = self.id_generator.generate()
        application: Application = Application(
            id=application_id,
            user_id=user_id,
            blood_type=blood_type,
            application_time=application_time,
            application_day=day_dt,
            slot_index=slot_index,
            location_id=location_id,
            status=status,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
        )
        await self.application_repository.save(application)
        return application