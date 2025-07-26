#!/usr/bin/env python3
"""
🚀 All-in-One Setup для Enhanced APatch Build
Автоматически создает и добавляет только нужные секреты для подписи
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

class EnhancedAPatchSetup:
    def __init__(self):
        self.repo = "AngelOfLlife/APatch"
        self.token = None
        self.temp_files = []
        
    def check_requirements(self):
        """Проверка всех требований"""
        print("🔍 Проверка требований...")
        
        # Проверить токен
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            print("❌ Не найден GITHUB_TOKEN")
            print("💡 Получите токен: https://github.com/settings/tokens")
            print("💡 Установите: export GITHUB_TOKEN=your_token")
            return False
            
        # Проверить keytool (Java)
        try:
            subprocess.run(['keytool', '-help'], capture_output=True, check=True)
            print("✅ Java keytool найден")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Java keytool не найден")
            print("💡 Установите Java JDK")
            return False
            
        # Проверить доступ к GitHub API
        try:
            headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get(f'https://api.github.com/repos/{self.repo}', headers=headers)
            if response.status_code == 200:
                print("✅ Доступ к GitHub API")
            else:
                print(f"❌ Ошибка доступа к GitHub API: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка подключения к GitHub: {e}")
            return False
            
        return True
    
    def generate_keystore(self):
        """Генерация keystore для подписи APK"""
        print("🔑 Генерация keystore для подписи...")
        
        # Параметры keystore
        keystore_info = {
            'password': 'apatch_enhanced_2024',
            'key_password': 'apatch_key_2024', 
            'alias': 'apatch_enhanced_key'
        }
        
        # Создать временный файл
        with tempfile.NamedTemporaryFile(suffix='.p12', delete=False) as temp_file:
            keystore_path = temp_file.name
            self.temp_files.append(keystore_path)
        
        # Команда для создания keystore
        cmd = [
            'keytool', '-genkeypair',
            '-keystore', keystore_path,
            '-storetype', 'PKCS12',
            '-storepass', keystore_info['password'],
            '-keypass', keystore_info['key_password'],
            '-alias', keystore_info['alias'],
            '-keyalg', 'RSA',
            '-keysize', '2048',
            '-validity', '10000',
            '-dname', 'CN=APatch Enhanced Build, OU=Development, O=APatch Community, L=Global, S=Development, C=WW'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ Keystore создан успешно")
            
            # Прочитать и закодировать keystore
            with open(keystore_path, 'rb') as f:
                keystore_data = f.read()
            
            keystore_base64 = base64.b64encode(keystore_data).decode('utf-8')
            
            return {
                'keystore_base64': keystore_base64,
                'store_password': keystore_info['password'],
                'key_password': keystore_info['key_password'],
                'alias': keystore_info['alias']
            }
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка создания keystore: {e.stderr}")
            return None
    
    def encrypt_secret(self, secret_value, public_key):
        """Шифрование секрета для GitHub"""
        public_key_obj = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
        box = public.SealedBox(public_key_obj)
        encrypted = box.encrypt(secret_value.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def add_github_secret(self, name, value):
        """Добавление секрета в GitHub"""
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Получить публичный ключ
        pub_key_url = f'https://api.github.com/repos/{self.repo}/actions/secrets/public-key'
        response = requests.get(pub_key_url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Ошибка получения публичного ключа для {name}")
            return False
            
        key_info = response.json()
        
        # Зашифровать секрет
        encrypted_value = self.encrypt_secret(value, key_info['key'])
        
        # Добавить секрет
        secret_url = f'https://api.github.com/repos/{self.repo}/actions/secrets/{name}'
        data = {
            'encrypted_value': encrypted_value,
            'key_id': key_info['key_id']
        }
        
        response = requests.put(secret_url, headers=headers, json=data)
        
        if response.status_code in [201, 204]:
            print(f"✅ Секрет {name} добавлен")
            return True
        else:
            print(f"❌ Ошибка добавления {name}: {response.text}")
            return False
    
    def setup_secrets(self, keystore_info):
        """Добавление всех секретов"""
        print("🔐 Добавление секретов в GitHub...")
        
        secrets = {
            'SIGNING_KEY': keystore_info['keystore_base64'],
            'KEY_STORE_PASSWORD': keystore_info['store_password'],
            'KEY_PASSWORD': keystore_info['key_password'],
            'ALIAS': keystore_info['alias']
        }
        
        success_count = 0
        total_secrets = len(secrets)
        
        for name, value in secrets.items():
            if self.add_github_secret(name, value):
                success_count += 1
        
        return success_count == total_secrets
    
    def cleanup(self):
        """Очистка временных файлов"""
        for temp_file in self.temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def run(self):
        """Основной процесс настройки"""
        print("🚀 Enhanced APatch Build - Автоматическая настройка")
        print("=" * 60)
        
        try:
            # Проверка требований
            if not self.check_requirements():
                return False
            
            print(f"📂 Репозиторий: {self.repo}")
            print(f"🔑 Токен: {'*' * (len(self.token)-8) + self.token[-8:]}")
            print()
            
            # Генерация keystore
            keystore_info = self.generate_keystore()
            if not keystore_info:
                return False
            
            # Добавление секретов
            if self.setup_secrets(keystore_info):
                print()
                print("=" * 60)
                print("🎉 НАСТРОЙКА ЗАВЕРШЕНА УСПЕШНО!")
                print()
                print("✅ Enhanced APatch Build готов:")
                print("   🔐 Keystore для подписи создан")
                print("   🔑 Все секреты добавлены в GitHub")
                print("   🛠️ Workflow готов к запуску")
                print()
                print("🚀 Следующие шаги:")
                print("   1. Перейдите: https://github.com/AngelOfLlife/APatch/actions")
                print("   2. Найдите workflow: 'Enhanced APatch Build'")
                print("   3. Запустите его вручную или создайте новый тег")
                print()
                print("🎯 Результат: APK с обходом проверки подписи!")
                return True
            else:
                print("❌ Ошибка добавления секретов")
                return False
                
        except KeyboardInterrupt:
            print("\n⏹️ Прервано пользователем")
            return False
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return False
        finally:
            self.cleanup()

def main():
    setup = EnhancedAPatchSetup()
    success = setup.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()