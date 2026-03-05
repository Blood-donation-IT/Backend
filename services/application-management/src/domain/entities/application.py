import datetime
from typing import Optional

class Application:
    def __init__(self, id: int,
                 user_id: int,
                 blood_type: str,
                 application_time: datetime.datetime,
                 application_day: Optional[datetime.datetime] = None,
                 slot_index: Optional[int] = None,
                 location_id: Optional[str] = None,
                 status: str = "pending",
                 description: Optional[str] = None,
                 created_at: Optional[datetime.datetime] = None,
                 updated_at: Optional[datetime.datetime] = None):
        self.id: int = id
        self.user_id: int = user_id
        self.blood_type: str = blood_type
        self.application_time: datetime.datetime = application_time
        self.application_day: Optional[datetime.datetime] = application_day
        self.slot_index: Optional[int] = slot_index  
        self.location_id: Optional[str] = location_id
        self.status: str = status
        self.description: Optional[str] = description
        self.created_at: Optional[datetime.datetime] = created_at
        self.updated_at: Optional[datetime.datetime] = updated_at
