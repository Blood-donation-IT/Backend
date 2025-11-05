# infrastructure/db/models/user_orm.py
from sqlalchemy import Column, String,BigInteger,Boolean,Integer,DateTime, UniqueConstraint,func
from user_profile_models.base import Base
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Any
class UserORM(Base):
    __tablename__ = "users_"

    id = Column(BigInteger, primary_key=True,autoincrement=False) #Snowflake ID
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    blood_type = Column(String, nullable=True) #A+, B-, etc
    is_verified = Column(Boolean, default=False, nullable=False)
    total_donations = Column(Integer, default=0, nullable=False)
    last_donation_at = Column(DateTime, nullable=True)
    roles = Column(ARRAY(String), default=["donor"], nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("id", "email", "phone", name="uix_users_identity"),
    )
    #TODO: replace dict with DTO dataclas
    def to_dict(self)->dict:
        # from domain.entities.user import User
        return{
            "id": self.id,
            "full_name": self.full_name,
            "email":self.email,
            "phone":self.phone,
            "blood_type":self.blood_type,
            "is_verified":self.is_verified,
            "total_donations":self.total_donations,
            "last_donation_at":self.last_donation_at,
            "roles":self.roles,
            "is_active":self.is_active,
            "is_banned":self.is_banned,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
        }
    @classmethod
    def from_entity(cls, user: Any) -> "UserORM":
        return cls(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            blood_type=user.blood_type,
            is_verified=user.is_verified,
            total_donations=user.total_donations,
            last_donation_at=user.last_donation_at,
            roles=user.roles,
            is_active=user.is_active,
            is_banned=user.is_banned,
        )