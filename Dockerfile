# Используем официальный образ Python
FROM python:3.11

# Установка необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright с поддержкой браузеров
RUN pip install playwright

# Создание виртуального окружения
RUN python -m venv /venv

# Установка зависимостей в виртуальное окружение
RUN /venv/bin/pip install pytest && /venv/bin/playwright install

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем ваши файлы в контейнер
COPY . .

# Указываем команду по умолчанию для запуска pytest из виртуального окружения
CMD ["/venv/bin/pytest", "test_two.py"]