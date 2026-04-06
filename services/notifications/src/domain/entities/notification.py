import datetime
from typing import Optional


class Notification:
    def __init__(
        self,
        id: int,
        user_id: int,
        title: str,
        message: str,
        created_at: Optional[datetime.datetime] = None,
        is_read: bool = False,
        type: int = 0,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.created_at = created_at
        self.is_read = is_read
        self.type = type
