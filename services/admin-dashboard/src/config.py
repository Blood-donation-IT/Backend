import os

class Config:
    SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")
    AUTHORIZATION_DATABASE_URL = os.getenv("AUTHORIZATION_DATABASE_URL")
    USER_PROFILE_DATABASE_URL = os.getenv("USER_PROFILE_DATABASE_URL")
    APPLICATION_MANAGEMENT_DATABASE_URL = os.getenv("APPLICATION_MANAGEMENT_DATABASE_URL")

    if not SECRET_KEY:
        raise ValueError("ADMIN_SECRET_KEY environment variable is not set")
    if not AUTHORIZATION_DATABASE_URL:
        raise ValueError("AUTHORIZATION_DATABASE_URL environment variable is not set")
    if not USER_PROFILE_DATABASE_URL:
        raise ValueError("USER_PROFILE_DATABASE_URL environment variable is not set")
    if not APPLICATION_MANAGEMENT_DATABASE_URL:
        raise ValueError("APPLICATION_MANAGEMENT_DATABASE_URL environment variable is not set")
