from sqlalchemy import Column, String, BigInteger, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuthorizationORM(Base):
    __tablename__ = "authorizations"
    __table_args__ = {'schema': None}  

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<AuthorizationORM(id={self.id}, email={self.email}, name={self.name})>'
