FROM python:3.12-slim

WORKDIR /app

COPY services/user-profile-migrations/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY libs/user-profile-models/ /app/libs/user-profile-models/
RUN pip install --no-cache-dir /app/libs/user-profile-models/

COPY services/user-profile-migrations/src /app/src
COPY services/user-profile-migrations/alembic.ini .

ENV PYTHONPATH=/app/src:/app/libs/user-profile-models/src

ENTRYPOINT ["alembic", "upgrade", "head"]