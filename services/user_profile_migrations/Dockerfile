FROM python:3.12-slim
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY libs/user_profile ./libs/user_profile
COPY services/user_profile_migrations ./service

RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install -e ./libs/user_profile

ENTRYPOINT ["alembic", "-c", "service/alembic.ini", "upgrade", "head"]