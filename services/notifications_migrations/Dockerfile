FROM python:3.12-slim
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY libs/notifications ./libs/notifications
COPY services/notifications_migrations ./service

RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install -e ./libs/notifications

ENTRYPOINT ["alembic", "-c", "service/alembic.ini", "upgrade", "head"]

