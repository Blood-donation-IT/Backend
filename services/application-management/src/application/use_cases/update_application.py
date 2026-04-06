from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.application import Application

import datetime
from typing import Optional

class UpdateApplicationUseCase:
    def __init__(self, repository: IApplicationRepository):
        self.repository = repository

    async def execute(self, 
                     application_id: int,
                     application_time: Optional[datetime.datetime] = None,
                     description: Optional[str] = None,
                     blood_type: Optional[str] = None,
                     status: Optional[str] = None) -> Application:
        
        application = await self.repository.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application with id {application_id} not found")
        
        if application_time:
            application.application_time = application_time
        if description:
            application.description = description
        if blood_type:
            application.blood_type = blood_type
        if status:
            application.status = status
        
        application.updated_at = datetime.datetime.utcnow() 
        
        await self.repository.update(application)
        return application