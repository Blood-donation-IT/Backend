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
                 password_hash: Optional[str] = None,
                 avatar_url: Optional[str] = None,
                 lives_saved_count: int = 0,
                 donor_status: Optional[str] = None,
                 has_donor_book: bool = False,
                 test_is_done: bool = False,
                 ):
        self.id: int = id
        self.full_name: str = full_name
        self.email: str = email
        self.phone: Optional[str] = phone
        self.blood_type: Optional[str] = blood_type
        self.avatar_url: Optional[str] = avatar_url
        self.is_verified: bool = is_verified
        self.total_donations: int = total_donations
        self.last_donation_at: Optional[datetime.datetime] = last_donation_at
        self.roles: Optional[list[str]] = roles or ["donor"]
        self.is_active: bool = is_active
        self.is_banned: bool = is_banned
        self.created_at: Optional[datetime.datetime] = created_at
        self.updated_at: Optional[datetime.datetime] = updated_at
        self.password_hash: Optional[str] = password_hash
        self.lives_saved_count: int = lives_saved_count
        self.donor_status: Optional[str] = donor_status
        self.has_donor_book: bool = has_donor_book
        self.test_is_done: bool = test_is_done
        
        
    @classmethod
    def from_orm_dict(cls, data: dict):
        return cls(**data)

   