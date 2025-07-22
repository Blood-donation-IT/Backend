import datetime
from dataclasses import dataclass

@dataclass
class User:
    def __init__(self, id: int,
                 full_name: str,
                 email: str,
                 blood_type: str = None,
                 is_verified: bool = False,
                 total_donations: int = 0,
                 last_donation_at: datetime.datetime = None,
                 
                 ):
        self.id:int = id
        self.full_name:str = full_name
        self.email:str = email
        self.blood_type:str = blood_type
        self.is_verified:bool = is_verified
        self.total_donations:int = total_donations
        self.last_donation_at:datetime.datetime = last_donation_at
        
        
        #??

   