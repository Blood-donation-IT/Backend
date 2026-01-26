import datetime
from typing import Optional

class User:
    def __init__(self, id: int,
                 full_name: str,
                 email: str,
                 phone: Optional[str] = None,
                 blood_type: Optional[str] = None,
                 is_verified: bool = False,
                 total_donations: int = 0,
                 last_donation_at: Optional[datetime.datetime] = None,
                 roles: Optional[list[str]] = None,
                 is_active: bool = True,
                 is_banned: bool = False,
                 created_at: Optional[datetime.datetime] = None,
                 updated_at: Optional[datetime.datetime] = None,
                 password_hash: Optional[str] = None
                 ):
        self.id:int = id
        self.full_name:str = full_name
        self.email:str = email
        self.phone:Optional[str] = phone
        self.blood_type:str = blood_type
        self.is_verified:bool = is_verified
        self.total_donations:int = total_donations
        self.last_donation_at:Optional[datetime.datetime] = last_donation_at
        self.roles:Optional[list[str]] = roles or ["donor"]
        self.is_active:bool = is_active
        self.is_banned:bool = is_banned
        self.created_at:Optional[datetime.datetime] = created_at
        self.updated_at:Optional[datetime.datetime] = updated_at
        self.password_hash:Optional[str] = password_hash
        
        
    @classmethod
    def from_orm_dict(cls, data: dict):
        return cls(**data)

   