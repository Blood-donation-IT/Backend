FROM python:3.13-slim

WORKDIR /app

COPY contracts ./contracts
COPY services/api_gateway ./service

RUN pip install --no-cache-dir -r service/requirements.txt

ENV PYTHONPATH=/app:/app/service/src
CMD ["python", "service/main.py"]