from abc import ABC, abstractmethod
from ..entities.application import Application
from typing import Optional, List
import datetime

class IApplicationRepository(ABC):
    @abstractmethod
    async def get_by_id(self, application_id: int) -> Optional[Application]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[Application]:
        pass

    @abstractmethod
    async def save(self, application: Application) -> None:
        pass

    @abstractmethod
    async def update(self, application: Application) -> None:
        pass

    @abstractmethod
    async def delete(self, application_id: int) -> None:
        pass