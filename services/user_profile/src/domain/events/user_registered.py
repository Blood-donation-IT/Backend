from src.domain.events.base import DomainEvent

class UserRegisteredEvent(DomainEvent):
    user_id: int
    email: str
    blood_type: str
    