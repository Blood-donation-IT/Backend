FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY libs/application_management ./libs/application_management
COPY services/application-management ./service
RUN pip install --no-cache-dir -r service/requirements.txt

RUN pip install -e ./contracts
RUN pip install -e ./libs/application_management
ENV PYTHONPATH=/app/service/src
CMD ["python", "service/main.py"]
