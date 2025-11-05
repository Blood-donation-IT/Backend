from dependency_injector import containers,providers

from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.services.i_event_publisher import IEventPublisher

from src.infrastructure.db.session import get_session
from src.infrastructure.repositories.sqlalchemy_user_repository import SQlAlchemyUserRepository
from src.domain.irepositories.i_user_repository import IUserRepository
from src.application.use_cases.create_user import CreateUserUseCase
from src.infrastructure.grpc.user_profile_server import UserProfileService
from src.infrastructure.kafka.producer import get_kafka_producer
from src.infrastructure.kafka.publisher import KafkaEventPublisher

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    # A-part
    db_session = providers.Resource(
        get_session
    )
    id_generator = providers.Singleton(
        SnowflakeIDGenerator,
        instance=1
    )
    
    sqlalchemy_repo_provider = providers.Factory(
        SQlAlchemyUserRepository,
        session=db_session
    )
    kafka_producer_resource= providers.Resource(
        get_kafka_producer
    )
    kafka_publishher_prodvider=providers.Factory(
        KafkaEventPublisher,
        producer=kafka_producer_resource
    )
    
    # B-part
    
    id_generator: providers.Provider[IIDGenerator] = providers.Selector(
        config.id_generator_type,
        snowflake=id_generator,
    )
    
    repository: providers.Provider[IUserRepository] = providers.Selector(
        config.repository_type,
        postgresql=sqlalchemy_repo_provider,
    )
    event_publisher: providers.Provider[IEventPublisher] = providers.Selector(
        config.event_publisher_type,
        kafka=kafka_publishher_prodvider,
    )
    
    # C-part
    create_user_uc = providers.Factory(
        CreateUserUseCase,
        repository=repository,
        id_generator=id_generator,
        event_publisher=event_publisher
    )
    
    user_profile_service = providers.Factory(
        UserProfileService,
        create_user_profile_use_case=create_user_uc
    )
    
    
    
        