from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.entities.user import User
from typing import Optional


class UpdateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository: IUserRepository = repository

    async def execute(
        self,
        user_id: int,
        name: Optional[str] = None,
        blood_type: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        if name is not None:
            user.name = name
        if blood_type is not None:
            user.blood_type = blood_type
        if avatar is not None:
            user.avatar = avatar
        await self.repository.update(user)
        return user
