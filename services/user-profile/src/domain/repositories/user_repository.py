from abc import ABC, abstractmethod
from models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass
    