#!/usr/bin/env python3
"""
🎯 Simple Classic Setup - Only Signing Secrets
Настройка только signing secrets для классического метода
APatch токены извлекаются автоматически из APK
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

class SimpleClassicSetup:
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
        
        keystore_path = "apatch_simple.p12"
        alias = "apatch-simple"
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
            '-dname', 'CN=APatch Simple, OU=Android, O=APatch, L=City, ST=State, C=US'
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Keystore создан: {keystore_path}")
            
            # Показываем информацию о ключе
            print("\n🔍 Информация о созданном ключе:")
            info_cmd = ['keytool', '-list', '-v', '-keystore', keystore_path, 
                       '-storepass', store_password, '-storetype', 'PKCS12']
            result = subprocess.run(info_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Извлекаем SHA256 fingerprint для информации
                for line in result.stdout.split('\n'):
                    if 'SHA256:' in line:
                        print(f"🔑 SHA256: {line.strip()}")
                        break
            
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

    def setup_signing_secrets(self):
        """Настраиваем только signing secrets"""
        print("🚀 Настройка signing secrets...")
        
        try:
            # Получаем публичный ключ
            public_key_data = self.get_github_public_key()
            print("✅ Публичный ключ репозитория получен")
            
            # Генерируем keystore
            signing_secrets = self.generate_keystore()
            if not signing_secrets:
                return False
            
            print(f"\n🔐 Добавляем {len(signing_secrets)} signing secrets в GitHub...")
            
            success_count = 0
            for secret_name, secret_value in signing_secrets.items():
                if self.add_github_secret(secret_name, secret_value, public_key_data):
                    success_count += 1
            
            print(f"\n✅ Успешно добавлено secrets: {success_count}/{len(signing_secrets)}")
            
            if success_count == len(signing_secrets):
                print("\n🎉 Все signing secrets настроены успешно!")
                print("🚀 Теперь можно запускать упрощенный классический workflow:")
                print(f"   https://github.com/{self.repo}/actions/workflows/classic_token_simple.yml")
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
        print("📋 УПРОЩЕННЫЙ КЛАССИЧЕСКИЙ WORKFLOW")
        print("="*60)
        print()
        print("🎯 Метод: Замена на собственную подпись:")
        print("  ✅ НЕ изменяет исходный код")
        print("  ✅ Сохраняет репозиторий чистым")
        print("  ✅ Автоматически извлекает APatch токены")
        print("  ✅ Заменяет подписи на собственную")
        print()
        print("🔄 Процесс:")
        print("  1. Собирает/загружает оригинальный APK")
        print("  2. Автоматически извлекает APatch токены")
        print("  3. Автоматически генерирует собственную подпись")
        print("  4. Заменяет APatch подписи на собственную")
        print("  5. Рекомпилирует и подписывает APK")
        print()
        print("🔐 Необходимые secrets (ТОЛЬКО 4 шт):")
        print("  🔑 Signing secrets:")
        print("    - SIGNING_KEY (автоматически)")
        print("    - KEY_STORE_PASSWORD (автоматически)")
        print("    - KEY_PASSWORD (автоматически)")
        print("    - ALIAS (автоматически)")
        print()
        print("✨ Особенности:")
        print("  - APatch токены извлекаются автоматически")
        print("  - Собственная подпись генерируется автоматически")
        print("  - Минимальная настройка (только signing)")
        print("  - Максимальная автоматизация")
        print()
        print(f"🚀 Запуск workflow:")
        print(f"   https://github.com/{self.repo}/actions/workflows/classic_token_simple.yml")

def main():
    print("🎯 Simple Classic APatch Setup")
    print("=" * 50)
    
    setup = SimpleClassicSetup()
    
    try:
        # Показываем информацию
        setup.show_workflow_info()
        
        # Проверяем требования
        if not setup.check_requirements():
            return
        
        print("\n" + "="*50)
        print("🚀 НАЧИНАЕМ УПРОЩЕННУЮ НАСТРОЙКУ")
        print("="*50)
        
        # Настраиваем только signing secrets
        if setup.setup_signing_secrets():
            print("\n🎉 Упрощенная настройка завершена успешно!")
            print("\n💡 APatch токены будут извлечены автоматически из APK")
            print("💡 Собственная подпись будет сгенерирована автоматически")
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