FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости для tkinter (GUI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk tk && \
    rm -rf /var/lib/apt/lists/*

# Копируем файлы приложения
COPY requirements.txt ./requirements.txt
COPY main.py ./main.py

# Ставим python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# По умолчанию запускаем тренажёр
CMD ["python", "main.py"]

