#!/usr/bin/env python3
"""
🚀 Classic Simple Build Launcher
Помощник для запуска упрощенного классического workflow
"""
import webbrowser
import sys
from urllib.parse import urlencode

def launch_workflow():
    """Открывает GitHub Actions для ручного запуска workflow"""
    
    print("🚀 Запуск упрощенного классического workflow APatch")
    print("=" * 60)
    
    # URL для запуска workflow
    base_url = "https://github.com/AngelOfLlife/APatch/actions/workflows/classic_token_simple.yml"
    
    print("📋 Информация о workflow:")
    print("  📁 Workflow: classic_token_simple.yml")
    print("  🎯 Метод: Замена на собственную подпись")
    print("  ✅ Источник: clean-token-setup ветка")
    print()
    
    print("🔐 Требуемые secrets:")
    print("  ✅ SIGNING_KEY - keystore в base64")
    print("  ✅ KEY_STORE_PASSWORD - пароль keystore")
    print("  ✅ KEY_PASSWORD - пароль ключа") 
    print("  ✅ ALIAS - алиас ключа")
    print()
    
    print("⚠️  ВАЖНО: Убедитесь что secrets настроены!")
    print("💡 Используйте: python3 setup_classic_simple.py")
    print()
    
    print("🌐 Открываю GitHub Actions в браузере...")
    print(f"🔗 URL: {base_url}")
    
    try:
        webbrowser.open(base_url)
        print("✅ Браузер открыт!")
    except Exception as e:
        print(f"❌ Не удалось открыть браузер: {e}")
        print(f"📋 Скопируйте URL вручную: {base_url}")
    
    print()
    print("📝 Инструкции по запуску:")
    print("1. В открывшейся странице нажмите 'Run workflow'")
    print("2. Убедитесь что выбрана ветка 'clean-token-setup'")
    print("3. Выберите источник APK:")
    print("   - 'build' - собрать из исходного кода (медленнее)")
    print("   - 'download_release' - скачать последний релиз (быстрее)")
    print("4. Нажмите 'Run workflow' для запуска")
    print()
    print("⏱️  Время выполнения: ~5-10 минут")
    print("📱 Результат: apatch-classic-signed.apk")
    print()
    print("🔍 Следить за процессом:")
    print("   https://github.com/AngelOfLlife/APatch/actions")

def show_secrets_info():
    """Показывает информацию о настройке secrets"""
    print("🔐 Настройка GitHub Secrets")
    print("=" * 40)
    print()
    print("📝 Необходимые secrets (только 4 шт):")
    print("  SIGNING_KEY - base64 encoded keystore")
    print("  KEY_STORE_PASSWORD - пароль keystore")
    print("  KEY_PASSWORD - пароль ключа")
    print("  ALIAS - алиас ключа в keystore")
    print()
    print("🚀 Автоматическая настройка:")
    print("  pip install PyNaCl")
    print("  export GITHUB_TOKEN=your_token")
    print("  python3 setup_classic_simple.py")
    print()
    print("🌐 Ручная настройка:")
    print("  https://github.com/AngelOfLlife/APatch/settings/secrets/actions")

def main():
    print("🎯 Classic Simple Build Launcher")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--secrets":
        show_secrets_info()
        return
    
    print()
    print("Выберите действие:")
    print("1. 🚀 Запустить workflow")
    print("2. 🔐 Информация о secrets")
    print("3. ❌ Выход")
    print()
    
    try:
        choice = input("Введите номер (1-3): ").strip()
        
        if choice == "1":
            launch_workflow()
        elif choice == "2":
            show_secrets_info()
        elif choice == "3":
            print("👋 До свидания!")
        else:
            print("❌ Неверный выбор")
            
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()