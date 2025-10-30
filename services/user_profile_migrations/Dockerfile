FROM python:3.12-slim
WORKDIR /app

COPY libs/user_profile ./libs/user_profile
COPY services/user_profile_migrations ./service

RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install  -e ./libs/user_profile


# ENV PYTHONPATH=/app/src:/app/libs/user-profile-models/src
#ENV DATABASE_URL=postgresql+psycopg2://user:password@user-profile-db:5432/user_profile_db
#RUN echo "DATABASE_URL in container: $DATABASE_URL"
ENTRYPOINT ["alembic", "-c", "service/alembic.ini", "upgrade", "head"]