from src.domain.events.base import DomainEvent

class UserRegisteredEvent(DomainEvent):
    user_id: id
    email: str
    blood_type: str
    