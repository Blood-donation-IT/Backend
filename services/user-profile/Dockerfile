FROM python:3.13-slim
WORKDIR /user-profile
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
