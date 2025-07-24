#!/bin/bash

# 🔑 Quick Add Extracted Secrets для APatch
# Быстрое добавление всех секретов с извлеченными подписями

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${PURPLE}"
    echo "🔑 Quick Add Extracted Secrets для APatch"
    echo "=========================================="
    echo "Быстрое добавление всех секретов с извлеченными подписями"
    echo "=========================================="
    echo -e "${NC}"
}

check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI не найден!${NC}"
        echo -e "${YELLOW}📥 Установите GitHub CLI:${NC}"
        echo "   • Linux: sudo apt install gh"
        echo "   • macOS: brew install gh"
        echo "   • Windows: scoop install gh"
        echo "   • Или скачайте: https://cli.github.com/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ GitHub CLI найден${NC}"
}

check_auth() {
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI не авторизован!${NC}"
        echo -e "${YELLOW}🔐 Авторизуйтесь:${NC}"
        echo "   gh auth login"
        exit 1
    fi
    
    echo -e "${GREEN}✅ GitHub CLI авторизован${NC}"
}

get_extracted_signatures() {
    echo -e "${CYAN}🔍 Введите извлеченные подписи из оригинального APK:${NC}"
    echo ""
    
    # APATCH_REAL_SIGNATURE
    echo -e "${YELLOW}📝 APATCH_REAL_SIGNATURE${NC}"
    echo "   Приоритетные варианты:"
    echo "   1. RSA сертификат (META-INF/ALIAS_AP.RSA): Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y="
    echo "   2. Встроенная подпись: 1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
    echo "   3. Signature File (META-INF/ALIAS_AP.SF): Sf8lTT4QszlGT6NOP8ltVuLmJpU="
    echo ""
    read -p "Введите APATCH_REAL_SIGNATURE (или Enter для RSA по умолчанию): " real_sig
    
    if [ -z "$real_sig" ]; then
        real_sig="Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y="
        echo -e "${GREEN}   Используется RSA сертификат по умолчанию${NC}"
    fi
    
    echo ""
    
    # APATCH_CODE_SIGNATURE
    echo -e "${YELLOW}📝 APATCH_CODE_SIGNATURE${NC}"
    echo "   Варианты:"
    echo "   1. SHA256 APK: w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc="
    echo "   2. SHA1 APK: CwsxhyPHS6AI0KQiw6TC7NE1Z4c="
    echo "   3. Свой вариант"
    echo ""
    read -p "Введите APATCH_CODE_SIGNATURE (или Enter для SHA256 по умолчанию): " code_sig
    
    if [ -z "$code_sig" ]; then
        code_sig="w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc="
        echo -e "${GREEN}   Используется SHA256 по умолчанию${NC}"
    fi
    
    echo ""
}

get_repository() {
    echo -e "${CYAN}📁 Укажите репозиторий:${NC}"
    echo ""
    read -p "Введите репозиторий (например: AngelOfLlife/APatch): " repo_input
    
    if [ -z "$repo_input" ]; then
        repo_input="AngelOfLlife/APatch"
        echo -e "${GREEN}   Используется репозиторий по умолчанию: $repo_input${NC}"
    fi
    
    # Проверяем доступ к репозиторию
    if ! gh repo view "$repo_input" &> /dev/null; then
        echo -e "${RED}❌ Нет доступа к репозиторию: $repo_input${NC}"
        echo "   Проверьте имя репозитория и права доступа"
        exit 1
    fi
    
    repository="$repo_input"
    echo -e "${GREEN}✅ Репозиторий доступен: $repository${NC}"
    echo ""
}

confirm_secrets() {
    echo -e "${PURPLE}📋 БУДУТ ДОБАВЛЕНЫ СЛЕДУЮЩИЕ СЕКРЕТЫ:${NC}"
    echo "======================================================"
    echo ""
    echo -e "${CYAN}🔐 Ключи подписи:${NC}"
    echo "   SIGNING_KEY: MIIKpAIBAzCCCk4GCSqGSIb3DQEHAaCCCj8Eggo7MII... (готовый keystore)"
    echo "   ALIAS: apatch"
    echo "   KEY_STORE_PASSWORD: apatch123"
    echo "   KEY_PASSWORD: apatch123"
    echo ""
    echo -e "${CYAN}🔍 Подписи APatch (извлеченные):${NC}"
    echo "   APATCH_REAL_SIGNATURE: $real_sig"
    echo "   APATCH_CODE_SIGNATURE: $code_sig"
    echo ""
    echo -e "${CYAN}📱 Информация о приложении:${NC}"
    echo "   APATCH_PACKAGE_NAME: me.bmax.apatch"
    echo "   APATCH_APP_CLASS: APApplication"
    echo "   APATCH_SIGNATURE_METHOD: verifyAppSignature"
    echo ""
    echo -e "${CYAN}🎯 Репозиторий:${NC} $repository"
    echo ""
    
    read -p "Продолжить добавление секретов? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⏹️  Операция отменена${NC}"
        exit 0
    fi
    echo ""
}

add_secrets() {
    echo -e "${BLUE}🚀 Добавляем секреты в репозиторий...${NC}"
    echo ""
    
    # Готовый SIGNING_KEY (keystore в base64)
    SIGNING_KEY="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"
    
    # Счетчики
    success_count=0
    total_count=9
    
    # Массив секретов
    declare -a secrets=(
        "SIGNING_KEY:$SIGNING_KEY"
        "ALIAS:apatch"
        "KEY_STORE_PASSWORD:apatch123"
        "KEY_PASSWORD:apatch123"
        "APATCH_REAL_SIGNATURE:$real_sig"
        "APATCH_CODE_SIGNATURE:$code_sig"
        "APATCH_PACKAGE_NAME:me.bmax.apatch"
        "APATCH_APP_CLASS:APApplication"
        "APATCH_SIGNATURE_METHOD:verifyAppSignature"
    )
    
    # Добавляем каждый секрет
    for secret_pair in "${secrets[@]}"; do
        key="${secret_pair%%:*}"
        value="${secret_pair#*:}"
        
        echo -e "${CYAN}📝 Добавляем $key...${NC}"
        
        if gh secret set "$key" --body "$value" --repo "$repository" 2>/dev/null; then
            echo -e "${GREEN}   ✅ $key добавлен успешно${NC}"
            ((success_count++))
        else
            echo -e "${RED}   ❌ Ошибка добавления $key${NC}"
        fi
    done
    
    echo ""
    echo -e "${PURPLE}📊 РЕЗУЛЬТАТ:${NC}"
    echo "=============="
    echo -e "${GREEN}✅ Успешно добавлено: $success_count/$total_count секретов${NC}"
    
    if [ $success_count -eq $total_count ]; then
        echo -e "${GREEN}🎉 ВСЕ СЕКРЕТЫ ДОБАВЛЕНЫ УСПЕШНО!${NC}"
        echo ""
        echo -e "${CYAN}🚀 Следующие шаги:${NC}"
        echo "   1. Перейдите в Actions вашего репозитория"
        echo "   2. Запустите любой workflow (например: ultimate_fix_apatch_build.yml)"
        echo "   3. Дождитесь сборки APK"
        echo "   4. Скачайте готовый APK без зависания!"
        echo ""
        echo -e "${PURPLE}🔗 Ссылки:${NC}"
        echo "   • Actions: https://github.com/$repository/actions"
        echo "   • Secrets: https://github.com/$repository/settings/secrets/actions"
    else
        echo -e "${YELLOW}⚠️  Некоторые секреты не добавлены${NC}"
        echo "   Проверьте права доступа к репозиторию"
        echo "   Или добавьте их вручную через веб-интерфейс"
    fi
}

show_manual_alternative() {
    echo ""
    echo -e "${PURPLE}📋 АЛЬТЕРНАТИВА - Ручное добавление через веб-интерфейс:${NC}"
    echo "======================================================"
    echo ""
    echo -e "${CYAN}🌐 Перейдите:${NC} https://github.com/$repository/settings/secrets/actions"
    echo ""
    echo -e "${CYAN}🔑 Добавьте эти секреты:${NC}"
    echo ""
    echo "SIGNING_KEY = $SIGNING_KEY"
    echo "ALIAS = apatch"
    echo "KEY_STORE_PASSWORD = apatch123"
    echo "KEY_PASSWORD = apatch123"
    echo "APATCH_REAL_SIGNATURE = $real_sig"
    echo "APATCH_CODE_SIGNATURE = $code_sig"
    echo "APATCH_PACKAGE_NAME = me.bmax.apatch"
    echo "APATCH_APP_CLASS = APApplication"
    echo "APATCH_SIGNATURE_METHOD = verifyAppSignature"
}

main() {
    print_banner
    
    # Проверки
    check_gh_cli
    check_auth
    
    # Сбор данных
    get_extracted_signatures
    get_repository
    
    # Подтверждение
    confirm_secrets
    
    # Добавление секретов
    add_secrets
    
    # Альтернативный способ
    show_manual_alternative
    
    echo ""
    echo -e "${GREEN}✨ Готово! Теперь можете запускать сборку APatch! ✨${NC}"
}

# Запуск основной функции
main "$@"