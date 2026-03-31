from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, Integer, func
from notifications_models.base import Base


class NotificationORM(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    user_id = Column(BigInteger, nullable=False, index=True)
    title = Column(String, nullable=False, default="")
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    type = Column(Integer, nullable=False, default=0)
