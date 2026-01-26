from dependency_injector import containers, providers

from src.infrastructure.db.base import get_session
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.domain.services.i_id_generator import IIDGenerator
from src.infrastructure.repositories.sqlalchemy_application_repository import SQLAlchemyApplicationRepository
from src.domain.irepositories.i_application_repository import IApplicationRepository
from src.application.use_cases.create_application import CreateApplicationUseCase
from src.application.use_cases.update_application import UpdateApplicationUseCase
from src.application.use_cases.get_application import GetApplicationUseCase
from src.infrastructure.grpc.application_management_server import ApplicationManagementService

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    # A-part
    db_session = providers.Resource(
        get_session
    )
    
    snowflake_id_generator = providers.Singleton(
        SnowflakeIDGenerator,
        instance=2
    )
    
    sqlalchemy_repo_provider = providers.Factory(
        SQLAlchemyApplicationRepository,
        session=db_session
    )
    
    # B-part
    
    id_generator: providers.Provider[IIDGenerator] = providers.Selector(
        config.id_generator_type,
        snowflake=snowflake_id_generator,
    )
    
    repository: providers.Provider[IApplicationRepository] = providers.Selector(
        config.repository_type,
        postgresql=sqlalchemy_repo_provider,
    )
    
    # C-part
    create_application_use_case = providers.Factory(
        CreateApplicationUseCase,
        repository=repository,
        id_generator=id_generator
    )
    
    update_application_use_case = providers.Factory(
        UpdateApplicationUseCase,
        repository=repository
    )
    
    get_application_use_case = providers.Factory(
        GetApplicationUseCase,
        repository=repository
    )
    
    application_management_service = providers.Factory(
        ApplicationManagementService,
        create_use_case=create_application_use_case,
        update_use_case=update_application_use_case,
        get_use_case=get_application_use_case,
        repository=repository
    )

