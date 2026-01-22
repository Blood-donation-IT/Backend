from dependency_injector import containers, providers

from src.infrastructure.db.base import get_session
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.domain.services.i_id_generator import IIDGenerator
from src.infrastructure.repositories.sqlalchemy_authorization_repository import SQLAlchemyAuthorizationRepository
from src.domain.irepositories.i_authorization_repository import IAuthorizationRepository
from src.application.use_cases.register_use_case import RegisterUseCase
from src.application.use_cases.login_use_case import LoginUseCase
from src.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from src.infrastructure.grpc.authorization_server import AuthorizationService

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    # A-part
    db_session = providers.Resource(
        get_session
    )
    
    snowflake_id_generator = providers.Singleton(
        SnowflakeIDGenerator,
        instance=1
    )
    
    sqlalchemy_repo_provider = providers.Factory(
        SQLAlchemyAuthorizationRepository,
        session=db_session
    )
    
    # B-part
    
    id_generator: providers.Provider[IIDGenerator] = providers.Selector(
        config.id_generator_type,
        snowflake=snowflake_id_generator,
    )
    
    repository: providers.Provider[IAuthorizationRepository] = providers.Selector(
        config.repository_type,
        postgresql=sqlalchemy_repo_provider,
    )
    
    # C-part
    register_use_case = providers.Factory(
        RegisterUseCase,
        repository=repository,
        id_generator=id_generator
    )
    
    login_use_case = providers.Factory(
        LoginUseCase,
        repository=repository
    )
    
    refresh_token_use_case = providers.Factory(
        RefreshTokenUseCase,
        repository=repository
    )
    
    authorization_service = providers.Factory(
        AuthorizationService,
        register_use_case=register_use_case,
        login_use_case=login_use_case,
        refresh_token_use_case=refresh_token_use_case
    )

