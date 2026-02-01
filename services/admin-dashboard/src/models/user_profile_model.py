from sqlalchemy import Column, String, BigInteger, Boolean, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users_"
    __table_args__ = {'schema': None}

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

    def __repr__(self):
        return f'<UserORM(id={self.id}, email={self.email}, full_name={self.full_name})>'
