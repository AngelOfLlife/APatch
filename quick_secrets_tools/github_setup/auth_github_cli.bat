@echo off
chcp 65001 > nul
title GitHub CLI Auth

echo.
echo 🔐 GitHub CLI Authorization
echo ===========================
echo.

gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI не найден!
    echo    Запустите: install_github_cli.bat
    pause
    exit /b 1
)

echo ✅ GitHub CLI найден
echo.

echo 👤 Пользователь: AngelOfLlife
echo 🔑 Токен: ВАШ_ТОКЕН_ЗДЕСЬ
echo.

echo 🚀 Запускаем авторизацию...
echo ВАШ_ТОКЕН_ЗДЕСЬ | gh auth login --with-token

if %errorlevel% equ 0 (
    echo ✅ Авторизация успешна!
    gh auth status
) else (
    echo ❌ Ошибка авторизации
    echo 💡 Убедитесь, что токен настроен через setup_token.bat
)

echo.
pause