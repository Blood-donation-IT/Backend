FROM python:3.11-slim

WORKDIR /app

COPY services/admin-dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/admin-dashboard /app/service
COPY libs /app/libs

ENV PYTHONPATH=/app/service/src:/app/libs

EXPOSE 5000

CMD ["python", "/app/service/main.py"]
