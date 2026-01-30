from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.entities.user import User
from typing import Optional


class UpdateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository: IUserRepository = repository

    async def execute(
        self,
        user_id: int,
        full_name: Optional[str] = None,
        blood_type: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> User:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        if full_name is not None:
            user.full_name = full_name
        if blood_type is not None:
            user.blood_type = blood_type
        if avatar_url is not None:
            user.avatar_url = avatar_url
        await self.repository.update(user)
        return user
