from abc import ABC, abstractmethod
from ..entities.user import User
from typing import Optional

class IAuthorizationRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass








