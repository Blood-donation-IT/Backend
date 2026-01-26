from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.entities.user import User
from typing import Optional

class GetUserByIdUseCase:
    def __init__(self, repository: IUserRepository):
        self.user_repository: IUserRepository = repository

    async def execute(self, user_id: int) -> Optional[User]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user
