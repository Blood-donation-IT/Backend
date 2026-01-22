from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.user import User
from src.infrastructure.services.password_service import PasswordService
import datetime
from typing import Optional
from google.protobuf.timestamp_pb2 import Timestamp

class RegisterUseCase:
    def __init__(self, repository: IAuthorizationRepository, id_generator: IIDGenerator):
        self.repository: IAuthorizationRepository = repository
        self.id_generator: IIDGenerator = id_generator

    async def execute(self,
                      email: str,
                      password: str,
                      name: str,
                      birth_date: Optional[Timestamp] = None,
                      created_at: Optional[datetime.datetime] = None,
                      updated_at: Optional[datetime.datetime] = None) -> User:
        existing_user = await self.repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        password_hash = PasswordService.hash_password(password)
        
        birth_date_dt: Optional[datetime.datetime] = None
        if birth_date:
            birth_date_dt = birth_date.ToDatetime()
        
        user_id: int = self.id_generator.generate()
        
        user: User = User(
            id=user_id,
            email=email,
            password_hash=password_hash,
            name=name,
            birth_date=birth_date_dt,
            created_at=created_at,
            updated_at=updated_at
        )

        await self.repository.save(user)
        return user




