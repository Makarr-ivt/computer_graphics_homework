FROM python:3.11-alpine

RUN apk add --no-cache ffmpeg

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
