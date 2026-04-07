FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY libs/authorization ./libs/authorization
COPY services/authorization ./service
RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install -e ./libs/authorization
ENV PYTHONPATH=/app:/app/service/src
CMD ["python", "service/main.py"]
