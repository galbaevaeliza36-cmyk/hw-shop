# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем все зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Открываем порт, на котором будет работать Django
EXPOSE 8000

# Команда для запуска Django (можно изменить на команду, которая нужна для твоего проекта)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]