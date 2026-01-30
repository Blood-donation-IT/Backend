import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "API Gateway"
    
    USER_SERVICE_HOST: str = "localhost" 
    USER_SERVICE_PORT: int = 50051
    
    APPLICATION_MANAGEMENT_SERVICE_HOST: str = "localhost"
    APPLICATION_MANAGEMENT_SERVICE_PORT: int = 50052
    
    AUTHORIZATION_SERVICE_HOST: str = "localhost"
    AUTHORIZATION_SERVICE_PORT: int = 50053
    
    SECRET_KEY: str = "blood-don"
    JWT_SECRET: str = "secret-key-for-testing"  # Має збігатися з authorization (JWT_SECRET)

    class Config:
        env_file = ".env"

settings = Settings()