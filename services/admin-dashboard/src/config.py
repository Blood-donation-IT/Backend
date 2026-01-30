import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    AUTHORIZATION_DATABASE_URL = os.getenv(
        'AUTHORIZATION_DATABASE_URL',
        'postgresql://user:password@authorization-db:5432/authorization_db'
    )
    
    USER_PROFILE_DATABASE_URL = os.getenv(
        'USER_PROFILE_DATABASE_URL',
        'postgresql://user:password@user-profile-db:5432/user_profile_db'
    )
    
    APPLICATION_MANAGEMENT_DATABASE_URL = os.getenv(
        'APPLICATION_MANAGEMENT_DATABASE_URL',
        'postgresql://user:password@application-management-db:5432/application_management_db'
    )
