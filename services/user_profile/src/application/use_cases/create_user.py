from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.user import User

import datetime
from typing import Optional
class CreateUserUseCase:
    def __init__(self, repository: IUserRepository,
                 id_generator: IIDGenerator):
        self.user_repository:IUserRepository = repository
        self.id_generator:IIDGenerator = id_generator
    async def execute(self,
                name: str,
                email: str,
                phone:Optional[str]=None,
                blood_type:Optional[str]=None,
                is_verified:bool=False,
                total_donations:int=0,
                last_donation_at:Optional[datetime.datetime]=None,
                roles: Optional[list[str]] = None,
                is_active: bool = True,
                is_banned: bool = False,
                created_at: Optional[datetime.datetime] = None,
                password_hash: Optional[str] = None,
                updated_at: Optional[datetime.datetime] = None,
                user_id: Optional[int] = None,
                avatar: Optional[str] = None)->User:
        
        if user_id is not None and user_id > 0:
            existing_by_id = await self.user_repository.get_user_by_id(user_id)
            if existing_by_id:
                return existing_by_id

        existing_by_email = await self.user_repository.get_user_by_email(email)
        if existing_by_email:
            if user_id and existing_by_email.id == user_id:
                return existing_by_email
            raise ValueError(f"User with email {email} already exists")

        if user_id is None:
            user_id = self.id_generator.generate()
        
        user: User = User(
            id=user_id,
            name=name,
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
            updated_at=updated_at,
            password_hash=password_hash if password_hash is not None else "",
            avatar=avatar,
        )
        await self.user_repository.save(user)
        return user
    
        