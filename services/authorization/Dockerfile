FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY libs/authorization_models ./libs/authorization_models
COPY services/authorization ./service
RUN pip install --no-cache-dir -r service/requirements.txt

RUN pip install  -e ./contracts
RUN pip install -e ./libs/authorization_models
# ENV PYTHONPATH=/app/service/src
CMD ["python", "service/main.py"]
