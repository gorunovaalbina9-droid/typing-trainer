@echo off
chcp 65001 >nul
echo Сборка тренажёра слепой печати...
echo.

pip install -r requirements.txt -q
if errorlevel 1 (
    echo Ошибка установки зависимостей
    pause
    exit /b 1
)

python -m PyInstaller --noconfirm --name "TypingTrainer" --onefile --windowed main.py

if exist "dist\TypingTrainer.exe" (
    echo.
    echo Готово! Исполняемый файл: dist\TypingTrainer.exe
    echo Файл progress.json будет создан рядом с exe при первом запуске.
) else (
    echo Сборка не удалась.
)

pause
