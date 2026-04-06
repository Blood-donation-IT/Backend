FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY libs/notifications ./libs/notifications
COPY services/notifications ./service
RUN pip install --no-cache-dir -r service/requirements.txt
RUN pip install -e ./contracts
RUN pip install -e ./libs/notifications
CMD ["python", "service/main.py"]
