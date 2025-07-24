@echo off
chcp 65001 > nul
title APatch Signature Extractor for Windows 10

echo.
echo 🖥️ APatch Signature Extractor for Windows 10
echo ===============================================
echo Быстрое извлечение подписей из оригинального APK
echo ===============================================
echo.

REM Проверяем наличие Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден в системе!
    echo.
    echo 📥 Установите Python:
    echo    1. Перейдите: https://www.python.org/downloads/
    echo    2. Скачайте Python 3.8 или новее
    echo    3. При установке ОБЯЗАТЕЛЬНО отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден в системе
python --version
echo.

REM Проверяем наличие скрипта
if not exist "windows_quick_extract.py" (
    echo ❌ Скрипт windows_quick_extract.py не найден!
    echo.
    echo 📥 Скачайте скрипт:
    echo    Файл должен находиться в той же папке что и этот .bat файл
    echo.
    pause
    exit /b 1
)

echo ✅ Скрипт найден
echo.

REM Проверяем аргументы командной строки
if "%~1"=="" (
    echo 📝 Использование:
    echo    extract_apatch_windows.bat "путь_к_apk_файлу"
    echo.
    echo 💡 Примеры:
    echo    extract_apatch_windows.bat APatch.apk
    echo    extract_apatch_windows.bat "C:\Downloads\APatch-11107-release.apk"
    echo.
    echo 🔍 Или перетащите APK файл на этот .bat файл
    echo.
    
    REM Запрашиваем путь к файлу у пользователя
    set /p apk_file="Введите путь к APK файлу: "
    if "!apk_file!"=="" (
        echo ❌ Путь к файлу не указан
        pause
        exit /b 1
    )
) else (
    set "apk_file=%~1"
)

REM Убираем кавычки из пути
set "apk_file=%apk_file:"=%"

echo.
echo 🔍 Анализируем файл: %apk_file%
echo.

REM Проверяем существование файла
if not exist "%apk_file%" (
    echo ❌ APK файл не найден: %apk_file%
    echo.
    echo 🔍 Проверьте:
    echo    • Правильность пути к файлу
    echo    • Существование файла
    echo    • Нет ли опечаток в имени
    echo.
    pause
    exit /b 1
)

echo ✅ APK файл найден
echo.

REM Запускаем анализ
echo 🚀 Запускаем извлечение подписей...
echo ====================================
echo.

python "windows_quick_extract.py" "%apk_file%"

set extract_result=%errorlevel%

echo.
echo ====================================

if %extract_result% equ 0 (
    echo ✅ ИЗВЛЕЧЕНИЕ ЗАВЕРШЕНО УСПЕШНО!
    echo.
    echo 📋 Следующие шаги:
    echo 1. Скопируйте значения APATCH_REAL_SIGNATURE и APATCH_CODE_SIGNATURE
    echo 2. Перейдите в настройки вашего GitHub репозитория
    echo 3. Обновите секреты новыми значениями
    echo 4. Запустите сборку APK
    echo.
    echo 🔗 Ссылка на секреты:
    echo    https://github.com/AngelOfLlife/APatch/settings/secrets/actions
    echo.
) else (
    echo ❌ ОШИБКА ПРИ ИЗВЛЕЧЕНИИ ПОДПИСЕЙ
    echo.
    echo 🆘 Попробуйте:
    echo    • Запустить от имени администратора
    echo    • Проверить целостность APK файла
    echo    • Убедиться что файл не поврежден
    echo.
)

echo 💡 Результаты также сохранены в текстовый файл
echo.

pause