# infrastructure/db/models/user_orm.py
from sqlalchemy import Column, String,BigInteger,Boolean,Integer,DateTime,func
from user_profile_models.base import Base
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Any
class UserORM(Base):
    __tablename__ = "users_"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    blood_type = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    total_donations = Column(Integer, default=0, nullable=False)
    last_donation_at = Column(DateTime, nullable=True)
    roles = Column(ARRAY(String), default=["donor"], nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    password_hash = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    lives_saved_count = Column(Integer, default=0, nullable=False)
    donor_status = Column(String, nullable=True)
    has_donor_book = Column(Boolean, default=False, nullable=False)
    test_is_done = Column(Boolean, default=False, nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "blood_type": self.blood_type,
            "is_verified": self.is_verified,
            "total_donations": self.total_donations,
            "last_donation_at": self.last_donation_at,
            "roles": self.roles,
            "is_active": self.is_active,
            "is_banned": self.is_banned,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "password_hash": self.password_hash,
            "avatar_url": self.avatar_url,
            "lives_saved_count": getattr(self, "lives_saved_count", 0) or 0,
            "donor_status": getattr(self, "donor_status", None),
            "has_donor_book": getattr(self, "has_donor_book", False) or False,
            "test_is_done": getattr(self, "test_is_done", False) or False,
            "birth_date": getattr(self, "birth_date", None),
        }

    @classmethod
    def from_entity(cls, user: Any) -> "UserORM":
        return cls(
            id=user.id,
            name=user.full_name,
            email=user.email,
            phone=user.phone,
            blood_type=user.blood_type,
            is_verified=user.is_verified,
            total_donations=user.total_donations,
            last_donation_at=user.last_donation_at,
            roles=user.roles,
            is_active=user.is_active,
            is_banned=user.is_banned,
            password_hash=user.password_hash if user.password_hash is not None else "",
            avatar_url=getattr(user, "avatar_url", None),
            lives_saved_count=getattr(user, "lives_saved_count", 0) or 0,
            donor_status=getattr(user, "donor_status", None),
            has_donor_book=getattr(user, "has_donor_book", False) or False,
            test_is_done=getattr(user, "test_is_done", False) or False,
            birth_date=getattr(user, "birth_date", None),
        )