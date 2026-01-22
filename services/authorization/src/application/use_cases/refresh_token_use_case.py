from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from src.infrastructure.services.jwt_service import JWTService
import datetime
from typing import Tuple

class RefreshTokenUseCase:
    def __init__(self, repository: IAuthorizationRepository):
        self.repository: IAuthorizationRepository = repository

    async def execute(self, refresh_token: str) -> Tuple[str, str, datetime.datetime]:

        payload = JWTService.verify_token(refresh_token)
        if not payload:
            raise ValueError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Token is not a refresh token")

        user_id = payload.get("user_id")
        email = payload.get("email")

        if not user_id or not email:
            raise ValueError("Invalid token payload")

        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        token_data = {"user_id": user.id, "email": user.email}
        new_access_token = JWTService.create_access_token(token_data)
        new_refresh_token = JWTService.create_refresh_token(token_data)

        expires_at = JWTService.get_token_expires_at(new_access_token)
        if not expires_at:
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        return (new_access_token, new_refresh_token, expires_at)








