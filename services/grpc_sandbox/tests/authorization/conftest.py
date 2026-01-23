import pytest
import os
import sys
import datetime
from unittest.mock import AsyncMock, MagicMock
from typing import Optional

conftest_file = os.path.abspath(__file__)
tests_dir = os.path.dirname(conftest_file)
grpc_sandbox_dir = os.path.dirname(os.path.dirname(tests_dir))
services_dir = os.path.dirname(grpc_sandbox_dir)
auth_dir = os.path.join(services_dir, 'authorization')
auth_dir = os.path.abspath(auth_dir)

if os.path.exists(auth_dir):
    if auth_dir not in sys.path:
        sys.path.insert(0, auth_dir)

from src.domain.entities.user import User
from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from src.domain.services.i_id_generator import IIDGenerator
from google.protobuf.timestamp_pb2 import Timestamp


@pytest.fixture(autouse=True)
def set_jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret-key-for-testing")


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=IAuthorizationRepository)


@pytest.fixture
def mock_id_generator():
    generator = MagicMock(spec=IIDGenerator)
    generator.generate.return_value = 123456789
    return generator


@pytest.fixture
def sample_user():
    return User(
        id=123456789,
        email="testuser@gmail.com",
        password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqJqJqJq",
        name="Test User",
        birth_date=datetime.datetime(1990, 1, 1),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )


@pytest.fixture
def sample_password():
    return "testpassword"


@pytest.fixture
def sample_birth_date():
    ts = Timestamp()
    ts.FromDatetime(datetime.datetime(1990, 1, 1))
    return ts
