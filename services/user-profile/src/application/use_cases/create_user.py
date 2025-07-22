from src.domain.irepositories.i_user_repository import IUserRepository
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.entities.user import User
import datetime
class CreateUserUseCase:
    def __init__(self, repository: IUserRepository,
                 id_generator: IIDGenerator):
        self.user_repository:IUserRepository = repository
        self.id_generator:IIDGenerator = id_generator
    def execute(self,
                full_name:str,
                email:str,
                blood_type:str|None=None,
                is_verified:bool=False,
                total_donations:int=0,
                last_donation_at:datetime.datetime|None=None)->int:
        user_id:int = self.id_generator.generate()
        user:User = User(
            id=user_id,
            full_name=full_name,
            email=email,
            blood_type=blood_type,
            is_verified=is_verified,
            total_donations=total_donations,
            last_donation_at=last_donation_at
        )
        self.user_repository.save(user)
        return user_id
    
        