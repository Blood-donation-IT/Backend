from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.constants import DAILY_CAPACITY
from src.domain.booking_rules import get_day_availability_reason
import datetime
import calendar


class GetCalendarAvailabilityUseCase:
    def __init__(self, repository: IApplicationRepository):
        self.repository = repository

    async def execute(self, year: int, month: int) -> list[str]: # повертаємо список дат
        today = datetime.date.today()
        _, last_day = calendar.monthrange(year, month)
        result = []
        for day in range(1, last_day + 1):
            d = datetime.date(year, month, day)
            if get_day_availability_reason(d, today) is not None:
                continue
            booked = await self.repository.count_booked_by_date(d)
            if booked < DAILY_CAPACITY: # хоча б одне вільне місце
                result.append(d.isoformat())
        return result
