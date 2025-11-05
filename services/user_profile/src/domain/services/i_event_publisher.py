from abc import ABC, abstractmethod

from src.domain.events.base import DomainEvent

class IEventPublisher(ABC):
    @abstractmethod
    async def publish(self, event:DomainEvent)->None:
        pass