FROM python:3.13-slim

COPY contracts ./contracts
COPY services/grpc-sandbox ./service
RUN pip install --no-cache-dir -r service/requirements.txt

RUN pip install  -e ./contracts

# WORKDIR /app/src

CMD ["python", "service/main.py"]