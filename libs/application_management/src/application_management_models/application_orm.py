from sqlalchemy import Column, String, BigInteger, DateTime, func
from application_management_models.base import Base
from typing import Optional


class ApplicationORM(Base):
    __tablename__ = "applications"

    id = Column(BigInteger, primary_key=True, autoincrement=False)  
    user_id = Column(BigInteger, nullable=False) 
    blood_type = Column(String, nullable=False)  
    application_time = Column(DateTime(timezone=True), nullable=False)
    application_day = Column(DateTime(timezone=True), nullable=True)
    location_id = Column(String, nullable=True)
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
            application_day=self.application_day,
            location_id=self.location_id,
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
            application_day=application.application_day,
            location_id=application.location_id,
            status=application.status,
            description=application.description
        )