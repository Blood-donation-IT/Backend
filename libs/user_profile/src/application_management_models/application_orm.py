from uuid import uuid4
from sqlalchemy import Column, String,BigInteger,Boolean,Integer,DateTime,func
import datetime
from infrastructure.db.base import Base
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.dialects.postgresql import ARRAY


class ApplicationORM(Base):
    __tablename__ = "applications"

    id = Column(BigInteger, primary_key=True, autoincrement=False)  
    user_id = Column(BigInteger, nullable=False) 
    blood_type = Column(String, nullable=False)  
    application_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="pending")
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_entity(self) -> "Application":
        from src.domain.entities.application import Application
        return Application(
            id=self.id,
            user_id=self.user_id,
            blood_type=self.blood_type,
            application_time=self.application_time,
            status=self.status,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_entity(cls, application: "Application") -> "ApplicationORM":
        return cls(
            id=application.id,
            user_id=application.user_id,
            blood_type=application.blood_type,
            application_time=application.application_time,
            status=application.status,
            description=application.description
        )