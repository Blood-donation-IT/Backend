FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY services/application-management ./service
RUN pip install --no-cache-dir -r service/requirements.txt

RUN pip install  -e ./contracts
# ENV PYTHONPATH=/app/service/src
CMD ["python", "service/main.py"]
