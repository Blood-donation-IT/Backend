from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.user import User
from src.domain.services.i_event_publisher import IEventPublisher
from src.domain.events.user_registered import UserRegisteredEvent

import datetime
from typing import Optional
class CreateUserUseCase:
    def __init__(self, repository: IUserRepository,
                 id_generator: IIDGenerator,
                 event_publisher: IEventPublisher):
        self.user_repository:IUserRepository = repository
        self.id_generator:IIDGenerator = id_generator
        self.event_publisher:IEventPublisher = event_publisher
    async def execute(self,
                full_name:str,
                email:str,
                phone:str,
                blood_type:Optional[str]=None,
                is_verified:bool=False,
                total_donations:int=0,
                last_donation_at:Optional[datetime.datetime]=None,
                roles: Optional[list[str]] = None,
                is_active: bool = True,
                is_banned: bool = False,
                created_at: Optional[datetime.datetime] = None,
                updated_at: Optional[datetime.datetime] = None)->User:
        user_id:int = self.id_generator.generate()
        user:User = User(
            id=user_id,
            full_name=full_name,
            email=email,
            phone=phone,
            blood_type=blood_type,
            is_verified=is_verified,
            total_donations=total_donations,
            last_donation_at=last_donation_at,
            roles=roles,
            is_active=is_active,
            is_banned=is_banned,
            created_at=created_at,
            updated_at=updated_at 
            
        )
        await self.user_repository.save(user)
        event:UserRegisteredEvent = UserRegisteredEvent(
            user_id=user.id,
            email=user.email,
            blood_type=user.blood_type
        )
        await self.event_publisher.publish(topic="user_registered",event=event)    
        return user
    
        