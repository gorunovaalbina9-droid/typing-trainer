# Тренажёр слепой печати — образ для запуска в Docker
# Требуется доступ к дисплею (X11) для GUI

FROM python:3.11-slim

# Tkinter требует tk и tcl
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    tcl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# PyInstaller не нужен в контейнере для запуска
RUN pip install --no-cache-dir \
    customtkinter>=5.2.0 \
    Pillow>=10.0.0 \
    matplotlib>=3.7.0

COPY main.py assets.py ./

# Папка assets создастся при первом запуске
RUN mkdir -p assets

ENTRYPOINT ["xvfb-run", "-a", "python", "main.py"]
