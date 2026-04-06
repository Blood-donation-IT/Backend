import datetime
from src.domain.constants import WEEKEND_WEEKDAYS, BOOKING_DAYS_AHEAD


def _to_date(d) -> datetime.date:
    return d.date() if hasattr(d, "date") else d


def is_weekend(d: datetime.date) -> bool:
    if hasattr(d, "weekday"):
        return d.weekday() in WEEKEND_WEEKDAYS
    return False # перевірка на вихідний день


def get_day_availability_reason(d: datetime.date, today: datetime.date | None = None) -> str | None: # причина недоступності слота
    if today is None:
        today = datetime.date.today()
    if d < today:
        return "past"
    if is_weekend(d):  # дата в минулому
        return "weekend" # вихідний
    max_date = today + datetime.timedelta(days=BOOKING_DAYS_AHEAD)
    if d > max_date:
        return "out_of_range" # більше ніж 2 місяці вперед
    return None


def is_date_in_booking_range(d: datetime.date, today: datetime.date | None = None) -> bool:
    return get_day_availability_reason(d, today) is None
