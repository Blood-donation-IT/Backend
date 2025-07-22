from abc import ABC, abstractmethod
from entities.user import User
from typing import Optional
import datetime
class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
    @abstractmethod
    def list_active_donors(self, limit: int = 100) -> list[User]:
        pass
    @abstractmethod
    def get_last_donation_date(self, user_id: int) -> Optional[datetime.datetime]:
        pass
    