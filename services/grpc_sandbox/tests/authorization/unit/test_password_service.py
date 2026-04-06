import pytest

from src.infrastructure.services.password_service import PasswordService


class TestPasswordService:

    def test_hash_password(self):
        password = "testpassword"
        hashed = PasswordService.hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert hashed.startswith("$2b$")
        assert len(hashed) > 50

    def test_verify_password_correct(self):
        password = "testpassword"
        hashed = PasswordService.hash_password(password)
        
        result = PasswordService.verify_password(password, hashed)
        assert result is True

    def test_verify_password_incorrect(self):
        password = "testpassword"
        wrong_password = "wrongpassword"
        hashed = PasswordService.hash_password(password)
        
        result = PasswordService.verify_password(wrong_password, hashed)
        assert result is False

    def test_hash_password_different_hashes(self):
        password = "testpassword"
        hashed1 = PasswordService.hash_password(password)
        hashed2 = PasswordService.hash_password(password)
        
        assert hashed1 != hashed2
        
        assert PasswordService.verify_password(password, hashed1) is True
        assert PasswordService.verify_password(password, hashed2) is True
