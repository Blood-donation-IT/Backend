# infrastructure/db/models/user_orm.py
from sqlalchemy import Column, String,BigInteger
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.db.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    email = Column(String)
    name = Column(String)
