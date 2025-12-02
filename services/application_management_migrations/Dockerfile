FROM python:3.12-slim
WORKDIR /app

COPY libs/application_management ./libs/application_management
COPY services/application_management_migrations ./service

RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install  -e ./libs/application_management


ENTRYPOINT ["alembic", "-c", "service/alembic.ini", "upgrade", "head"]