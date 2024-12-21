# Используем официальный образ Python
FROM python:3.11

# Установка необходимых зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright с поддержкой браузеров
RUN pip install playwright pytest && playwright install

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем ваши файлы в контейнер
COPY . .

# Указываем команду по умолчанию для запуска pytest
CMD ["pytest", "test_two.py"]
