import pytest
import datetime
from unittest.mock import AsyncMock
from google.protobuf.timestamp_pb2 import Timestamp

from src.application.use_cases.register_use_case import RegisterUseCase
from src.domain.entities.user import User
from src.infrastructure.services.password_service import PasswordService


@pytest.mark.asyncio
class TestRegisterUseCase:

    async def test_register_user_success(self, mock_repository, mock_id_generator, sample_birth_date):
        mock_repository.get_by_email.return_value = None
        mock_repository.save = AsyncMock()
        
        use_case = RegisterUseCase(repository=mock_repository, id_generator=mock_id_generator)
        
        user = await use_case.execute(
            email="testuser@gmail.com",
            password="testpassword",
            name="Test User",
            birth_date=sample_birth_date
        )
        
        assert user is not None
        assert user.email == "testuser@gmail.com"
        assert user.name == "Test User"
        assert user.id == 123456789
        assert user.password_hash is not None
        assert user.password_hash != "testpassword"
        assert PasswordService.verify_password("testpassword", user.password_hash)
        mock_repository.get_by_email.assert_called_once_with("testuser@gmail.com")
        mock_repository.save.assert_called_once()

    async def test_register_user_email_already_exists(self, mock_repository, mock_id_generator, sample_user):
        mock_repository.get_by_email.return_value = sample_user
        
        use_case = RegisterUseCase(repository=mock_repository, id_generator=mock_id_generator)
        
        with pytest.raises(ValueError, match="User with email .* already exists"):
            await use_case.execute(
                email="testuser@gmail.com",
                password="testpassword",
                name="Test User"
            )

    async def test_register_user_without_birth_date(self, mock_repository, mock_id_generator):
        mock_repository.get_by_email.return_value = None
        mock_repository.save = AsyncMock()
        
        use_case = RegisterUseCase(repository=mock_repository, id_generator=mock_id_generator)
        
        user = await use_case.execute(
            email="testuser@gmail.com",
            password="testpassword",
            name="Test User"
        )
        
        assert user is not None
        assert user.birth_date is None

    async def test_register_user_password_is_hashed(self, mock_repository, mock_id_generator):
        mock_repository.get_by_email.return_value = None
        mock_repository.save = AsyncMock()
        
        use_case = RegisterUseCase(repository=mock_repository, id_generator=mock_id_generator)
        
        user = await use_case.execute(
            email="testuser@gmail.com",
            password="testpassword",
            name="Test User"
        )
        
        assert user.password_hash != "testpassword"
        assert user.password_hash.startswith("$2b$")
        assert PasswordService.verify_password("testpassword", user.password_hash)
