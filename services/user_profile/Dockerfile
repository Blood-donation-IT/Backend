FROM alpine:3.20 AS downloader
RUN apk add --no-cache wget
RUN wget -O /grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.11/grpc_health_probe-linux-amd64
RUN chmod +x /grpc_health_probe

FROM python:3.13-slim
WORKDIR /app
COPY contracts ./contracts
COPY services/user-profile ./service
RUN pip install --no-cache-dir -r service/requirements.txt
COPY --from=downloader /grpc_health_probe /bin/grpc_health_probe
RUN pip install  -e ./contracts
# ENV PYTHONPATH=/app/service/src
CMD ["python", "service/main.py"]
