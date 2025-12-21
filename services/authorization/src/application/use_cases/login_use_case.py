from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService
from src.domain.entities.user import User
import datetime
from typing import Tuple

class LoginUseCase:
    def __init__(self, repository: IAuthorizationRepository):
        self.repository: IAuthorizationRepository = repository

    async def execute(self, email: str, password: str) -> Tuple[User, str, str, datetime.datetime]:
    
        user = await self.repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not PasswordService.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        token_data = {"user_id": user.id, "email": user.email}
        access_token = JWTService.create_access_token(token_data)
        refresh_token = JWTService.create_refresh_token(token_data)
        
        expires_at = JWTService.get_token_expires_at(access_token)
        if not expires_at:
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        return (user, access_token, refresh_token, expires_at)

