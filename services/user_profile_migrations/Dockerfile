FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY libs/user-profile-models /libs/user-profile-models
RUN pip install -e ./libs/user-profile-models


ENV PYTHONPATH=/app/src:/app/libs/user-profile-models/src

ENTRYPOINT ["alembic", "upgrade", "head"]