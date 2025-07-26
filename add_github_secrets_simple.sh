#!/bin/bash

# 🔐 Простое добавление GitHub Secrets для Enhanced APatch Build
# Только секреты для подписи APK - токены замены больше не нужны!

set -e

echo "🚀 Enhanced APatch Build - Настройка GitHub Secrets"
echo "============================================================"

# Проверить наличие токена
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Не найден GITHUB_TOKEN в переменных окружения"
    echo "💡 Установите: export GITHUB_TOKEN=your_token"
    exit 1
fi

# Определить репозиторий
REPO="AngelOfLlife/APatch"

echo "📂 Репозиторий: $REPO"
echo "🔑 Токен: ${GITHUB_TOKEN:0:8}************${GITHUB_TOKEN: -8}"
echo

# Проверить наличие gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) не найден"
    echo "💡 Установите: https://cli.github.com/"
    exit 1
fi

# Проверить наличие keytool
if ! command -v keytool &> /dev/null; then
    echo "❌ keytool не найден"
    echo "💡 Установите Java JDK"
    exit 1
fi

echo "🔑 Генерация нового keystore для подписи..."

# Параметры keystore
KEYSTORE_PASSWORD="apatch123456"
KEY_PASSWORD="apatch123456"
ALIAS="apatch_key"

# Создать временный keystore
keytool -genkeypair \
    -keystore temp_keystore.p12 \
    -storetype PKCS12 \
    -storepass "$KEYSTORE_PASSWORD" \
    -keypass "$KEY_PASSWORD" \
    -alias "$ALIAS" \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -dname "CN=APatch Enhanced, OU=Development, O=APatch, L=Unknown, S=Unknown, C=US"

if [ $? -eq 0 ]; then
    echo "✅ Keystore создан успешно"
else
    echo "❌ Ошибка создания keystore"
    exit 1
fi

# Закодировать keystore в base64
KEYSTORE_BASE64=$(base64 -w 0 temp_keystore.p12)

# Удалить временный файл
rm temp_keystore.p12

echo
echo "📋 Добавление секретов для подписи APK:"
echo "   🔐 SIGNING_KEY - Keystore для подписи APK"
echo "   🔑 KEY_STORE_PASSWORD - Пароль keystore"
echo "   🔑 KEY_PASSWORD - Пароль ключа"
echo "   🏷️ ALIAS - Алиас ключа"
echo

# Установить репозиторий для gh CLI
export GH_TOKEN="$GITHUB_TOKEN"
export GH_REPO="$REPO"

# Добавить секреты
echo "🔐 Добавление SIGNING_KEY..."
echo "$KEYSTORE_BASE64" | gh secret set SIGNING_KEY

echo "🔑 Добавление KEY_STORE_PASSWORD..."
echo "$KEYSTORE_PASSWORD" | gh secret set KEY_STORE_PASSWORD

echo "🔑 Добавление KEY_PASSWORD..."
echo "$KEY_PASSWORD" | gh secret set KEY_PASSWORD

echo "🏷️ Добавление ALIAS..."
echo "$ALIAS" | gh secret set ALIAS

echo
echo "============================================================"
echo "🎉 ВСЕ СЕКРЕТЫ ДОБАВЛЕНЫ УСПЕШНО!"
echo
echo "✅ Enhanced APatch Build готов к запуску:"
echo "   • Workflow будет использовать новый keystore"
echo "   • APK будет правильно подписан"
echo "   • Проверка подписи APatch будет обойдена в коде"
echo
echo "🚀 Теперь можно запускать workflow!"
echo "🔗 https://github.com/$REPO/actions"