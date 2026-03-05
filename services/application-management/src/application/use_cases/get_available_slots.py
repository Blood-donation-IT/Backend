from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.constants import (
    SLOT_TIME_LABELS,
    SLOT_CAPACITY,
    DAILY_CAPACITY,
    NUM_SLOTS,
)

import datetime
from typing import List


def _to_date(d: datetime.datetime) -> datetime.date:
    return d.date() if hasattr(d, "date") else d


class GetAvailableSlotsUseCase:
    def __init__(self, repository: IApplicationRepository):
        self.repository = repository

    async def execute(self, date: datetime.datetime) -> dict:
        date_only = _to_date(date)
        daily_booked = await self.repository.count_booked_by_date(date_only)
        slots = []
        for slot_index in range(NUM_SLOTS):
            booked = await self.repository.count_booked_by_date_and_slot(
                date_only, slot_index
            )
            capacity = SLOT_CAPACITY
            is_available = booked < capacity
            slots.append({
                "slot_index": slot_index,
                "time_label": SLOT_TIME_LABELS[slot_index],
                "booked_count": booked,
                "capacity": capacity,
                "is_available": is_available,
            })
        return {
            "slots": slots,
            "daily_booked": daily_booked,
            "daily_capacity": DAILY_CAPACITY,
        }
