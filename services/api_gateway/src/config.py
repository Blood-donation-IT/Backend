import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "API Gateway"
    
    USER_SERVICE_HOST: str = "localhost" 
    USER_SERVICE_PORT: int = 50051       

    SECRET_KEY: str = "blood-don"
    
    class Config:
        env_file = ".env"

settings = Settings()