from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, func

from user_profile_models.base import Base


class HealthTestResultORM(Base):

    __tablename__ = "health_test_results"

    user_id = Column(BigInteger, ForeignKey("users_.id", ondelete="CASCADE"), primary_key=True)
    completed_at = Column(DateTime(timezone=True), nullable=False)
    q1 = Column(Boolean, nullable=False)
    q2 = Column(Boolean, nullable=False)
    q3 = Column(Boolean, nullable=False)
    q4 = Column(Boolean, nullable=False)
    q5 = Column(Boolean, nullable=False)
    q6 = Column(Boolean, nullable=False)
    blood_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
