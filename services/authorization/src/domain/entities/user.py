import datetime
from typing import Optional

class User:
    def __init__(self, 
                 id: int,
                 email: str,
                 password_hash: str,
                 name: str,
                 birth_date: Optional[datetime.datetime] = None,
                 created_at: Optional[datetime.datetime] = None,
                 updated_at: Optional[datetime.datetime] = None):
        self.id: int = id
        self.email: str = email
        self.password_hash: str = password_hash
        self.name: str = name
        self.birth_date: Optional[datetime.datetime] = birth_date
        self.created_at: Optional[datetime.datetime] = created_at
        self.updated_at: Optional[datetime.datetime] = updated_at




