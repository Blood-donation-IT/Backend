from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.entities.application import Application
from typing import AsyncGenerator

class GetApplicationUseCase:
    def __init__(self, repository: IApplicationRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> AsyncGenerator[Application, None]:
        async for application in self.repository.find_by_user_id(user_id):
            yield application