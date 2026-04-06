FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY libs/user_profile ./libs/user_profile
COPY services/user_profile ./service
RUN pip install --no-cache-dir -r service/requirements.txt

RUN pip install  -e ./contracts
RUN pip install  -e ./libs/user_profile

# ENV PYTHONPATH=/app/service/src
CMD ["python", "service/main.py"]
