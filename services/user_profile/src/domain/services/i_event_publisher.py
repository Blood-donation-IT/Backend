from abc import ABC, abstractmethod
from pydantic import BaseModel

class DomainEvent(BaseModel):
    pass

class IEventPublisher(ABC):
    @abstractmethod
    async def publish(self, event:DomainEvent)->None:
        pass