FROM python:3.12-slim
WORKDIR /app

COPY libs/authorization ./libs/authorization
COPY services/authorization_migrations ./service

RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install -e ./libs/authorization


ENTRYPOINT ["alembic", "-c", "service/alembic.ini", "upgrade", "head"]