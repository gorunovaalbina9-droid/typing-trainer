@echo off
chcp 65001 >nul
title Тренажёр слепой печати

echo Запуск тренажёра...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не найден.
    echo.
    echo Установите Python с https://www.python.org/downloads/
    echo При установке отметьте "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if not exist "main.py" (
    echo Ошибка: файл main.py не найден. Запустите run.bat из папки с приложением.
    pause
    exit /b 1
)

if not exist ".installed" (
    echo Первый запуск: устанавливаем зависимости...
    pip install -r requirements.txt -q
    if errorlevel 1 (
        echo Ошибка установки. Проверьте подключение к интернету.
        pause
        exit /b 1
    )
    echo. > .installed
)

python main.py

if errorlevel 1 (
    echo.
    echo Программа завершилась с ошибкой.
    pause
)
