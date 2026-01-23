import pytest
import datetime
from unittest.mock import AsyncMock

from src.application.use_cases.login_use_case import LoginUseCase
from src.infrastructure.services.password_service import PasswordService
from src.infrastructure.services.jwt_service import JWTService


@pytest.mark.asyncio
class TestLoginUseCase:

    async def test_login_success(self, mock_repository, sample_user, sample_password):
        hashed_password = PasswordService.hash_password(sample_password)
        sample_user.password_hash = hashed_password
        
        mock_repository.get_by_email.return_value = sample_user
        
        use_case = LoginUseCase(repository=mock_repository)
        
        user, access_token, refresh_token, expires_at = await use_case.execute(
            email="testuser@gmail.com",
            password=sample_password
        )
        
        assert user is not None
        assert user.email == "testuser@gmail.com"
        assert access_token is not None
        assert refresh_token is not None
        assert isinstance(expires_at, datetime.datetime)
        assert expires_at > datetime.datetime.utcnow()
        
        access_payload = JWTService.verify_token(access_token)
        assert access_payload is not None
        assert access_payload["user_id"] == user.id
        assert access_payload["email"] == user.email
        
        refresh_payload = JWTService.verify_token(refresh_token)
        assert refresh_payload is not None
        assert refresh_payload["type"] == "refresh"

    async def test_login_user_not_found(self, mock_repository, sample_password):
        mock_repository.get_by_email.return_value = None
        
        use_case = LoginUseCase(repository=mock_repository)
        
        with pytest.raises(ValueError, match="Invalid email or password"):
            await use_case.execute(
                email="testuser@gmail.com",
                password=sample_password
            )

    async def test_login_wrong_password(self, mock_repository, sample_user):
        hashed_password = PasswordService.hash_password("testpassword")
        sample_user.password_hash = hashed_password
        
        mock_repository.get_by_email.return_value = sample_user
        
        use_case = LoginUseCase(repository=mock_repository)
        
        with pytest.raises(ValueError, match="Invalid email or password"):
            await use_case.execute(
                email="testuser@gmail.com",
                password="wrongpassword"
            )
