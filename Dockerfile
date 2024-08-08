# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONPATH=/code

# Команда для запуска бота
CMD ["python", "-m", "app.main"]
