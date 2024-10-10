FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0"]