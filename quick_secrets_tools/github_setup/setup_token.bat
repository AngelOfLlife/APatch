@echo off
chcp 65001 > nul
title GitHub Token Setup

echo.
echo 🔑 GitHub Token Setup Script
echo =============================
echo.

echo 📋 Данные для настройки:
echo    Пользователь: AngelOfLlife
echo    Репозиторий: AngelOfLlife/APatch
echo.

echo 🔑 ВВЕДИТЕ ВАШ GITHUB ТОКЕН:
echo    Формат: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
echo    (ваш токен указан в файле INSTALL.md)
echo.
set /p user_token="Введите токен: "

if "%user_token%"=="" (
    echo ❌ Токен не может быть пустым!
    pause
    exit /b 1
)

echo.
echo 🔄 Настраиваем токен в файлах...

powershell -Command "(Get-Content 'auth_github_cli.bat') -replace 'ВАШ_ТОКЕН_ЗДЕСЬ', '%user_token%' | Set-Content 'auth_github_cli.bat'"
powershell -Command "(Get-Content 'auth_github_cli.sh') -replace 'ВАШ_ТОКЕН_ЗДЕСЬ', '%user_token%' | Set-Content 'auth_github_cli.sh'"

echo ✅ Токен настроен!
echo.
echo 🚀 Следующие шаги:
echo    1. install_github_cli.bat
echo    2. auth_github_cli.bat  
echo    3. cd .. ^&^& quick_add_extracted_secrets.bat
echo.
pause