# Используем официальный образ Python
FROM python:3.9-slim-buster

# Create app directory and new user
RUN mkdir /app && \
    useradd -u 1000 -G users -U -m -s /bin/bash feiman && \
    chown feiman:feiman /app
# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
USER feiman
ENV PATH=/home/feiman/.local/bin:$PATH
# Копируем файлы требований
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip3 install --upgrade pip wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Копируем исходный код в контейнер
COPY src/ /app/src/

# Запускаем приложение
CMD ["python", "src/bot.py"]
