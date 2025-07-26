#!/usr/bin/env python3
"""
🎯 Setup Classic Token Replacement Secrets
Настройка GitHub secrets для классического метода с 5 токенами APatch
"""
import subprocess
import requests
import json
import base64
import os
import sys
import tempfile
from pathlib import Path

try:
    from nacl import encoding, public
except ImportError:
    print("❌ Не установлена библиотека PyNaCl")
    print("💡 Установите: pip install PyNaCl")
    sys.exit(1)

class ClassicAPatchSetup:
    def __init__(self):
        self.repo = "AngelOfLlife/APatch"
        self.token = None
        self.temp_files = []

    def check_requirements(self):
        print("🔍 Проверка требований...")
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            print("❌ Не найден GITHUB_TOKEN")
            print("💡 Получите токен: https://github.com/settings/tokens")
            print("💡 Установите: export GITHUB_TOKEN=your_token")
            return False

        try:
            subprocess.run(['keytool', '-help'], capture_output=True, check=True)
            print("✅ Java keytool найден")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Java keytool не найден")
            print("💡 Установите Java JDK")
            return False

        return True

    def get_github_public_key(self):
        """Получаем публичный ключ репозитория для шифрования"""
        url = f'https://api.github.com/repos/{self.repo}/actions/secrets/public-key'
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"❌ Ошибка получения публичного ключа: {response.text}")

    def encrypt_secret(self, public_key_data, secret_value):
        """Шифруем secret для GitHub"""
        public_key = public.PublicKey(public_key_data['key'], encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    def add_github_secret(self, secret_name, secret_value, public_key_data):
        """Добавляем secret в GitHub"""
        url = f'https://api.github.com/repos/{self.repo}/actions/secrets/{secret_name}'
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        encrypted_value = self.encrypt_secret(public_key_data, secret_value)
        
        data = {
            'encrypted_value': encrypted_value,
            'key_id': public_key_data['key_id']
        }
        
        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [201, 204]:
            print(f"✅ Secret {secret_name} добавлен")
            return True
        else:
            print(f"❌ Ошибка добавления {secret_name}: {response.text}")
            return False

    def generate_keystore(self):
        """Генерируем новый keystore"""
        print("🔑 Генерируем новый keystore...")
        
        keystore_path = "apatch_classic.p12"
        alias = "apatch-classic"
        store_password = "apatch123456"
        key_password = "apatch123456"
        
        # Удаляем существующий keystore
        if os.path.exists(keystore_path):
            os.remove(keystore_path)
        
        # Генерируем новый keystore
        cmd = [
            'keytool', '-genkeypair',
            '-alias', alias,
            '-keyalg', 'RSA',
            '-keysize', '2048',
            '-validity', '10000',
            '-keystore', keystore_path,
            '-storetype', 'PKCS12',
            '-storepass', store_password,
            '-keypass', key_password,
            '-dname', 'CN=APatch Classic, OU=Android, O=APatch, L=Moscow, ST=Moscow, C=RU'
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Keystore создан: {keystore_path}")
            
            # Кодируем в base64
            with open(keystore_path, 'rb') as f:
                keystore_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            self.temp_files.append(keystore_path)
            
            return {
                'SIGNING_KEY': keystore_b64,
                'KEY_STORE_PASSWORD': store_password,
                'KEY_PASSWORD': key_password,
                'ALIAS': alias
            }
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка создания keystore: {e}")
            return None

    def get_apatch_tokens(self):
        """Получаем стандартные токены APatch (можно настроить)"""
        print("🎯 Настройка токенов APatch...")
        
        tokens = {
            'APATCH_REAL_SIGNATURE': 'sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4=',
            'APATCH_CODE_SIGNATURE': '1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=',
            'APATCH_PACKAGE_NAME': 'me.bmax.apatch',
            'APATCH_APP_CLASS': 'APApplication',
            'APATCH_SIGNATURE_METHOD': 'verifySignature'
        }
        
        print("📋 Стандартные токены APatch:")
        for key, value in tokens.items():
            print(f"  {key}: {value}")
        
        # Возможность настройки пользователем
        print("\n💡 Хотите изменить какие-либо токены? (y/n): ", end="")
        if input().lower() == 'y':
            for key in tokens:
                print(f"\n🔧 {key} (текущее: {tokens[key]})")
                new_value = input("Новое значение (Enter - оставить как есть): ").strip()
                if new_value:
                    tokens[key] = new_value
        
        return tokens

    def setup_all_secrets(self):
        """Настраиваем все необходимые secrets"""
        print("🚀 Настройка всех secrets для классического метода...")
        
        try:
            # Получаем публичный ключ
            public_key_data = self.get_github_public_key()
            print("✅ Публичный ключ репозитория получен")
            
            # Генерируем keystore
            signing_secrets = self.generate_keystore()
            if not signing_secrets:
                return False
            
            # Получаем токены APatch
            apatch_tokens = self.get_apatch_tokens()
            
            # Объединяем все secrets
            all_secrets = {**signing_secrets, **apatch_tokens}
            
            print(f"\n🔐 Добавляем {len(all_secrets)} secrets в GitHub...")
            
            success_count = 0
            for secret_name, secret_value in all_secrets.items():
                if self.add_github_secret(secret_name, secret_value, public_key_data):
                    success_count += 1
            
            print(f"\n✅ Успешно добавлено secrets: {success_count}/{len(all_secrets)}")
            
            if success_count == len(all_secrets):
                print("\n🎉 Все secrets настроены успешно!")
                print("🚀 Теперь можно запускать классический workflow:")
                print(f"   https://github.com/{self.repo}/actions/workflows/classic_token_apatch_build.yml")
                return True
            else:
                print("\n⚠️ Некоторые secrets не удалось добавить")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка настройки secrets: {e}")
            return False

    def cleanup(self):
        """Очищаем временные файлы"""
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"🗑️ Удален временный файл: {file_path}")
                except:
                    pass

    def show_workflow_info(self):
        """Показываем информацию о workflow"""
        print("\n" + "="*60)
        print("📋 ИНФОРМАЦИЯ О КЛАССИЧЕСКОМ WORKFLOW")
        print("="*60)
        print()
        print("🎯 Классический метод с токенами:")
        print("  ✅ НЕ изменяет исходный код")
        print("  ✅ Сохраняет репозиторий чистым")
        print("  ✅ Работает с готовым APK")
        print()
        print("🔄 Процесс:")
        print("  1. Собирает/загружает оригинальный APK")
        print("  2. Извлекает токены из APK автоматически")
        print("  3. Декомпилирует APK в smali код")
        print("  4. Заменяет 5 токенов в smali файлах")
        print("  5. Рекомпилирует APK")
        print("  6. Подписывает новым ключом")
        print()
        print("🔐 Необходимые secrets:")
        print("  📝 APatch токены (5 шт):")
        print("    - APATCH_REAL_SIGNATURE")
        print("    - APATCH_CODE_SIGNATURE")
        print("    - APATCH_PACKAGE_NAME")
        print("    - APATCH_APP_CLASS")
        print("    - APATCH_SIGNATURE_METHOD")
        print()
        print("  🔑 Signing secrets (4 шт):")
        print("    - SIGNING_KEY")
        print("    - KEY_STORE_PASSWORD")
        print("    - KEY_PASSWORD")
        print("    - ALIAS")
        print()
        print(f"🚀 Запуск workflow:")
        print(f"   https://github.com/{self.repo}/actions/workflows/classic_token_apatch_build.yml")

def main():
    print("🎯 Classic APatch Token Replacement Setup")
    print("=" * 50)
    
    setup = ClassicAPatchSetup()
    
    try:
        # Показываем информацию
        setup.show_workflow_info()
        
        # Проверяем требования
        if not setup.check_requirements():
            return
        
        print("\n" + "="*50)
        print("🚀 НАЧИНАЕМ НАСТРОЙКУ")
        print("="*50)
        
        # Настраиваем secrets
        if setup.setup_all_secrets():
            print("\n🎉 Настройка завершена успешно!")
        else:
            print("\n❌ Настройка завершена с ошибками")
            
    except KeyboardInterrupt:
        print("\n❌ Настройка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
    finally:
        setup.cleanup()

if __name__ == "__main__":
    main()