#!/bin/bash

# 🔐 Быстрая настройка всех секретов для AngelOfLlife/APatch
# Запустите этот скрипт для автоматического добавления всех секретов

set -e

echo "🚀 Настройка секретов для AngelOfLlife/APatch"
echo "============================================="

# Проверяем наличие GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI не установлен!"
    echo "📥 Установите: https://cli.github.com/"
    exit 1
fi

# Проверяем авторизацию
if ! gh auth status &> /dev/null; then
    echo "🔑 Выполните авторизацию в GitHub CLI:"
    gh auth login
fi

echo ""
echo "📋 Добавляем все секреты в AngelOfLlife/APatch..."
echo ""

# Добавляем все секреты
echo "1/9 Добавляем SIGNING_KEY..."
gh secret set SIGNING_KEY --repo AngelOfLlife/APatch --body "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"

echo "2/9 Добавляем ALIAS..."
gh secret set ALIAS --repo AngelOfLlife/APatch --body "apatch"

echo "3/9 Добавляем KEY_STORE_PASSWORD..."
gh secret set KEY_STORE_PASSWORD --repo AngelOfLlife/APatch --body "apatch123"

echo "4/9 Добавляем KEY_PASSWORD..."
gh secret set KEY_PASSWORD --repo AngelOfLlife/APatch --body "apatch123"

echo "5/9 Добавляем APATCH_REAL_SIGNATURE..."
gh secret set APATCH_REAL_SIGNATURE --repo AngelOfLlife/APatch --body "sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4="

echo "6/9 Добавляем APATCH_CODE_SIGNATURE..."
gh secret set APATCH_CODE_SIGNATURE --repo AngelOfLlife/APatch --body "1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="

echo "7/9 Добавляем APATCH_PACKAGE_NAME..."
gh secret set APATCH_PACKAGE_NAME --repo AngelOfLlife/APatch --body "me.bmax.apatch"

echo "8/9 Добавляем APATCH_APP_CLASS..."
gh secret set APATCH_APP_CLASS --repo AngelOfLlife/APatch --body "APApplication"

echo "9/9 Добавляем APATCH_SIGNATURE_METHOD..."
gh secret set APATCH_SIGNATURE_METHOD --repo AngelOfLlife/APatch --body "verifyAppSignature"

echo ""
echo "✅ Все секреты успешно добавлены!"
echo ""

# Проверяем добавленные секреты
echo "🔍 Проверяем добавленные секреты:"
gh secret list --repo AngelOfLlife/APatch

echo ""
echo "🎉 Готово! Все 9 секретов добавлены в AngelOfLlife/APatch"
echo ""
echo "🚀 Следующие шаги:"
echo "   1. Создайте workflow файл в .github/workflows/"
echo "   2. Перейдите в Actions: https://github.com/AngelOfLlife/APatch/actions"
echo "   3. Запустите сборку APatch"
echo "   4. Скачайте готовый APK без зависания!"
echo ""
echo "🔗 Полезные ссылки:"
echo "   • Секреты: https://github.com/AngelOfLlife/APatch/settings/secrets/actions"
echo "   • Actions: https://github.com/AngelOfLlife/APatch/actions"
echo "   • Настройки: https://github.com/AngelOfLlife/APatch/settings"