from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "API Gateway"
    
    USER_SERVICE_HOST: str = "user-profile"
    USER_SERVICE_PORT: int = 50051
    
    APPLICATION_MANAGEMENT_SERVICE_HOST: str = "application-management"
    APPLICATION_MANAGEMENT_SERVICE_PORT: int = 50052
    
    AUTHORIZATION_SERVICE_HOST: str = "authorization"
    AUTHORIZATION_SERVICE_PORT: int = 50053

    NOTIFICATIONS_SERVICE_HOST: str = "notifications"
    NOTIFICATIONS_SERVICE_PORT: int = 50054

    OAUTH_SERVICE_HOST: str = "oauth"
    OAUTH_SERVICE_PORT: int = 50055
    
    SECRET_KEY: str
    JWT_SECRET: str  # Має збігатися з authorization (JWT_SECRET)

    class Config:
        env_file = ".env"

settings = Settings()