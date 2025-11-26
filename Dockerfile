FROM python:3.13.7-slim

WORKDIR /photo-bucket-fastapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "80"]