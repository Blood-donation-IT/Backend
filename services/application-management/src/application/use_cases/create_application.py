from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.application import Application


import datetime
from typing import Optional
class CreateApplicationUseCase:
    def __init__(self, repository: IApplicationRepository, id_generator: IIDGenerator):
        self.application_repository: IApplicationRepository = repository
        self.id_generator: IIDGenerator = id_generator

    async def execute(self,
                      user_id: int,
                      blood_type: str,
                      description: str,
                      status: str,
                      created_at: Optional[datetime.datetime] = None,
                      updated_at: Optional[datetime.datetime] = None) -> Application:
        application_id: int = self.id_generator.generate()
        
        application: Application = Application(
            id=application_id,
            user_id=user_id,
            blood_type=blood_type,
            status=status,
            description=description,
            created_at=created_at,
            updated_at=updated_at 
        )

        await self.application_repository.save(application)
        return application