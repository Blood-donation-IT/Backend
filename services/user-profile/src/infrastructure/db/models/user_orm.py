# infrastructure/db/models/user_orm.py
from sqlalchemy import Column, String,BigInteger,Boolean,Integer,DateTime
import datetime
from infrastructure.db.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    blood_type = Column(String, nullable=True) #A+, B-, etc
    is_verified = Column(Boolean, default=False, nullable=False)
    total_donations = Column(Integer, default=0, nullable=False)
    last_donation_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    
