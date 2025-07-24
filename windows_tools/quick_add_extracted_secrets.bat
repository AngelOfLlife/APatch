@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Quick Add Extracted Secrets для APatch

echo.
echo 🔑 Quick Add Extracted Secrets для APatch
echo ==========================================
echo Быстрое добавление всех секретов с извлеченными подписями
echo ==========================================
echo.

REM Проверяем наличие GitHub CLI
gh --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI не найден!
    echo.
    echo 📥 Установите GitHub CLI:
    echo    • Скачайте: https://cli.github.com/
    echo    • Windows: winget install GitHub.cli
    echo    • Chocolatey: choco install gh
    echo.
    pause
    exit /b 1
)

echo ✅ GitHub CLI найден

REM Проверяем авторизацию
gh auth status > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ GitHub CLI не авторизован!
    echo.
    echo 🔐 Авторизуйтесь:
    echo    gh auth login
    echo.
    pause
    exit /b 1
)

echo ✅ GitHub CLI авторизован
echo.

REM Получаем извлеченные подписи
echo 🔍 Введите извлеченные подписи из оригинального APK:
echo.

echo 📝 APATCH_REAL_SIGNATURE
echo    Приоритетные варианты:
echo    1. RSA сертификат (META-INF/ALIAS_AP.RSA): Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y=
echo    2. Встроенная подпись: 1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=
echo    3. Signature File (META-INF/ALIAS_AP.SF): Sf8lTT4QszlGT6NOP8ltVuLmJpU=
echo.
set /p real_sig="Введите APATCH_REAL_SIGNATURE (Enter = RSA по умолчанию): "

if "!real_sig!"=="" (
    set "real_sig=Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y="
    echo    ✅ Используется RSA сертификат по умолчанию
)

echo.

echo 📝 APATCH_CODE_SIGNATURE
echo    Варианты:
echo    1. SHA256 APK: w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc=
echo    2. SHA1 APK: CwsxhyPHS6AI0KQiw6TC7NE1Z4c=
echo    3. Свой вариант
echo.
set /p code_sig="Введите APATCH_CODE_SIGNATURE (Enter = SHA256 по умолчанию): "

if "!code_sig!"=="" (
    set "code_sig=w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc="
    echo    ✅ Используется SHA256 по умолчанию
)

echo.

REM Получаем репозиторий
echo 📁 Укажите репозиторий:
echo.
set /p repository="Введите репозиторий (Enter = AngelOfLlife/APatch): "

if "!repository!"=="" (
    set "repository=AngelOfLlife/APatch"
    echo    ✅ Используется репозиторий по умолчанию: !repository!
)

echo.

REM Проверяем доступ к репозиторию
gh repo view "!repository!" > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Нет доступа к репозиторию: !repository!
    echo    Проверьте имя репозитория и права доступа
    pause
    exit /b 1
)

echo ✅ Репозиторий доступен: !repository!
echo.

REM Подтверждение
echo 📋 БУДУТ ДОБАВЛЕНЫ СЛЕДУЮЩИЕ СЕКРЕТЫ:
echo ======================================================
echo.
echo 🔐 Ключи подписи:
echo    SIGNING_KEY: MIIKpAIBAzCCCk4GCSqGSIb3DQEHAaCCCj8Eggo7MII... (готовый keystore)
echo    ALIAS: apatch
echo    KEY_STORE_PASSWORD: apatch123
echo    KEY_PASSWORD: apatch123
echo.
echo 🔍 Подписи APatch (извлеченные):
echo    APATCH_REAL_SIGNATURE: !real_sig!
echo    APATCH_CODE_SIGNATURE: !code_sig!
echo.
echo 📱 Информация о приложении:
echo    APATCH_PACKAGE_NAME: me.bmax.apatch
echo    APATCH_APP_CLASS: APApplication
echo    APATCH_SIGNATURE_METHOD: verifyAppSignature
echo.
echo 🎯 Репозиторий: !repository!
echo.

set /p confirm="Продолжить добавление секретов? (y/N): "
if /i not "!confirm!"=="y" (
    echo ⏹️  Операция отменена
    pause
    exit /b 0
)

echo.

REM Добавляем секреты
echo 🚀 Добавляем секреты в репозиторий...
echo.

REM Готовый SIGNING_KEY
set "SIGNING_KEY=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"

set success_count=0
set total_count=9

REM Добавляем секреты по одному
echo 📝 Добавляем SIGNING_KEY...
gh secret set SIGNING_KEY --body "!SIGNING_KEY!" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ SIGNING_KEY добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления SIGNING_KEY
)

echo 📝 Добавляем ALIAS...
gh secret set ALIAS --body "apatch" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ ALIAS добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления ALIAS
)

echo 📝 Добавляем KEY_STORE_PASSWORD...
gh secret set KEY_STORE_PASSWORD --body "apatch123" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ KEY_STORE_PASSWORD добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления KEY_STORE_PASSWORD
)

echo 📝 Добавляем KEY_PASSWORD...
gh secret set KEY_PASSWORD --body "apatch123" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ KEY_PASSWORD добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления KEY_PASSWORD
)

echo 📝 Добавляем APATCH_REAL_SIGNATURE...
gh secret set APATCH_REAL_SIGNATURE --body "!real_sig!" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ APATCH_REAL_SIGNATURE добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления APATCH_REAL_SIGNATURE
)

echo 📝 Добавляем APATCH_CODE_SIGNATURE...
gh secret set APATCH_CODE_SIGNATURE --body "!code_sig!" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ APATCH_CODE_SIGNATURE добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления APATCH_CODE_SIGNATURE
)

echo 📝 Добавляем APATCH_PACKAGE_NAME...
gh secret set APATCH_PACKAGE_NAME --body "me.bmax.apatch" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ APATCH_PACKAGE_NAME добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления APATCH_PACKAGE_NAME
)

echo 📝 Добавляем APATCH_APP_CLASS...
gh secret set APATCH_APP_CLASS --body "APApplication" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ APATCH_APP_CLASS добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления APATCH_APP_CLASS
)

echo 📝 Добавляем APATCH_SIGNATURE_METHOD...
gh secret set APATCH_SIGNATURE_METHOD --body "verifyAppSignature" --repo "!repository!" > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ APATCH_SIGNATURE_METHOD добавлен успешно
    set /a success_count+=1
) else (
    echo    ❌ Ошибка добавления APATCH_SIGNATURE_METHOD
)

echo.
echo 📊 РЕЗУЛЬТАТ:
echo ==============
echo ✅ Успешно добавлено: !success_count!/%total_count% секретов

if !success_count! equ %total_count% (
    echo.
    echo 🎉 ВСЕ СЕКРЕТЫ ДОБАВЛЕНЫ УСПЕШНО!
    echo.
    echo 🚀 Следующие шаги:
    echo    1. Перейдите в Actions вашего репозитория
    echo    2. Запустите любой workflow (например: ultimate_fix_apatch_build.yml)
    echo    3. Дождитесь сборки APK
    echo    4. Скачайте готовый APK без зависания!
    echo.
    echo 🔗 Ссылки:
    echo    • Actions: https://github.com/!repository!/actions
    echo    • Secrets: https://github.com/!repository!/settings/secrets/actions
) else (
    echo.
    echo ⚠️  Некоторые секреты не добавлены
    echo    Проверьте права доступа к репозиторию
    echo    Или добавьте их вручную через веб-интерфейс
)

echo.
echo 📋 АЛЬТЕРНАТИВА - Ручное добавление через веб-интерфейс:
echo ======================================================
echo.
echo 🌐 Перейдите: https://github.com/!repository!/settings/secrets/actions
echo.
echo 🔑 Добавьте эти секреты:
echo.
echo SIGNING_KEY = !SIGNING_KEY:~0,50!...
echo ALIAS = apatch
echo KEY_STORE_PASSWORD = apatch123
echo KEY_PASSWORD = apatch123
echo APATCH_REAL_SIGNATURE = !real_sig!
echo APATCH_CODE_SIGNATURE = !code_sig!
echo APATCH_PACKAGE_NAME = me.bmax.apatch
echo APATCH_APP_CLASS = APApplication
echo APATCH_SIGNATURE_METHOD = verifyAppSignature

echo.
echo ✨ Готово! Теперь можете запускать сборку APatch! ✨
echo.
pause