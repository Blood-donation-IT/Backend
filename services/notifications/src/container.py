from dependency_injector import containers, providers

from src.infrastructure.db.base import get_session
from src.infrastructure.id_generator.snowflake_generator import SnowflakeIDGenerator
from src.domain.services.i_id_generator import IIDGenerator
from src.domain.irepositories.i_notification_repository import INotificationRepository
from src.infrastructure.repositories.sqlalchemy_notification_repository import (
    SQLAlchemyNotificationRepository,
)
from src.application.use_cases.create_notification import CreateNotificationUseCase
from src.application.use_cases.get_notifications import GetNotificationsUseCase
from src.application.use_cases.mark_as_read import MarkAsReadUseCase
from src.infrastructure.grpc.notifications_server import NotificationsService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_session = providers.Resource(get_session)

    snowflake_id_generator = providers.Singleton(SnowflakeIDGenerator, instance=4)

    sqlalchemy_repo_provider = providers.Factory(
        SQLAlchemyNotificationRepository,
        session=db_session,
    )

    id_generator: providers.Provider[IIDGenerator] = providers.Selector(
        config.id_generator_type,
        snowflake=snowflake_id_generator,
    )

    repository: providers.Provider[INotificationRepository] = providers.Selector(
        config.repository_type,
        postgresql=sqlalchemy_repo_provider,
    )

    create_notification_use_case = providers.Factory(
        CreateNotificationUseCase,
        repository=repository,
        id_generator=id_generator,
    )
    get_notifications_use_case = providers.Factory(
        GetNotificationsUseCase,
        repository=repository,
    )
    mark_as_read_use_case = providers.Factory(
        MarkAsReadUseCase,
        repository=repository,
    )

    notifications_service = providers.Factory(
        NotificationsService,
        get_notifications_use_case=get_notifications_use_case,
        mark_as_read_use_case=mark_as_read_use_case,
        create_notification_use_case=create_notification_use_case,
    )
