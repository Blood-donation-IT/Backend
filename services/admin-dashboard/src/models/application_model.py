from sqlalchemy import Column, String, BigInteger, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApplicationORM(Base):
    __tablename__ = "applications"
    __table_args__ = {'schema': None}  

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

    def __repr__(self):
        return f'<ApplicationORM(id={self.id}, user_id={self.user_id}, status={self.status})>'
