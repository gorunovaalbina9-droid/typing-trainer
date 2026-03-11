@echo off
chcp 65001 >nul
echo ═════════════════════════════════════════
echo   Сборка тренажёра для распространения
echo ═════════════════════════════════════════
echo.

pip install -r requirements.txt -q
if errorlevel 1 (
    echo Ошибка установки зависимостей
    pause
    exit /b 1
)
python -m PyInstaller --noconfirm --name "TypingTrainer" --onefile --windowed --hidden-import=PIL --hidden-import=matplotlib --collect-data matplotlib main.py
if errorlevel 1 (
    echo Сборка не удалась.
    pause
    exit /b 1
)

if not exist "dist\TypingTrainer.exe" (
    echo Ошибка: exe не найден.
    pause
    exit /b 1
)

echo.
echo Создание архива TypingTrainer.zip...

cd dist
if exist TypingTrainer.zip del TypingTrainer.zip
copy ..\ИНСТРУКЦИЯ.txt "Как пользоваться.txt" >nul 2>&1
powershell -Command "Compress-Archive -Path 'TypingTrainer.exe','Как пользоваться.txt' -DestinationPath 'TypingTrainer.zip' -Force"
del "Как пользоваться.txt" >nul 2>&1
cd ..

echo.
echo ✓ Готово!
echo.
echo   • exe-файл:       dist\TypingTrainer.exe
echo   • архив для раздачи: dist\TypingTrainer.zip
echo.
echo Передайте пользователю TypingTrainer.zip или TypingTrainer.exe
echo
pause
