import datetime
from typing import Optional

class Application:
    def __init__(self, id: int,
                 user_id: int,
                 blood_type: str,
                 application_time: datetime.datetime,
                 status: str,
                 description: str,
                 created_at: Optional[datetime.datetime] = None,
                 updated_at: Optional[datetime.datetime] = None):
        self.id: int = id
        self.user_id: int = user_id
        self.blood_type: str = blood_type
        self.application_time: datetime.datetime = application_time
        self.status: str = status
        self.description: str = description
        self.created_at: Optional[datetime.datetime] = created_at 
        self.updated_at: Optional[datetime.datetime] = updated_at 
