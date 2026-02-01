from sqlalchemy import Column, String, BigInteger, DateTime, func
from authorization_models.base import Base
from typing import Any, Optional
import datetime

class AuthorizationORM(Base):
    __tablename__ = "authorizations"

    id = Column(BigInteger, primary_key=True, autoincrement=False)  # Snowflake ID
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_entity(cls, user: Any) -> "AuthorizationORM":
        return cls(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            name=user.name,
        )





