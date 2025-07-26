#!/usr/bin/env python3
"""
🔐 Добавление GitHub Secrets для Enhanced APatch Build
Только секреты для подписи APK - токены замены больше не нужны!
"""

import requests
import json
import base64
import os
import sys
from nacl import encoding, public
import subprocess
from pathlib import Path

class EnhancedSecretsManager:
    def __init__(self, token, repo):
        self.token = token
        self.repo = repo
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = f'https://api.github.com/repos/{repo}'
        
    def get_public_key(self):
        """Получить публичный ключ репозитория для шифрования секретов"""
        url = f'{self.base_url}/actions/secrets/public-key'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"❌ Ошибка получения публичного ключа: {response.text}")
    
    def encrypt_secret(self, secret_value, public_key):
        """Зашифровать секрет с помощью публичного ключа"""
        public_key_obj = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
        box = public.SealedBox(public_key_obj)
        encrypted = box.encrypt(secret_value.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def add_secret(self, secret_name, secret_value):
        """Добавить секрет в репозиторий"""
        try:
            # Получить публичный ключ
            key_info = self.get_public_key()
            public_key = key_info['key']
            key_id = key_info['key_id']
            
            # Зашифровать секрет
            encrypted_value = self.encrypt_secret(secret_value, public_key)
            
            # Добавить секрет
            url = f'{self.base_url}/actions/secrets/{secret_name}'
            data = {
                'encrypted_value': encrypted_value,
                'key_id': key_id
            }
            
            response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code in [201, 204]:
                print(f"✅ Секрет {secret_name} добавлен успешно")
                return True
            else:
                print(f"❌ Ошибка добавления секрета {secret_name}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при добавлении секрета {secret_name}: {e}")
            return False

    def generate_keystore(self):
        """Генерация нового keystore для подписи"""
        print("🔑 Генерация нового keystore...")
        
        keystore_password = "apatch123456"
        key_password = "apatch123456" 
        alias = "apatch_key"
        
        # Создать временный keystore
        cmd = [
            'keytool', '-genkeypair',
            '-keystore', 'temp_keystore.p12',
            '-storetype', 'PKCS12',
            '-storepass', keystore_password,
            '-keypass', key_password,
            '-alias', alias,
            '-keyalg', 'RSA',
            '-keysize', '2048',
            '-validity', '10000',
            '-dname', 'CN=APatch Enhanced, OU=Development, O=APatch, L=Unknown, S=Unknown, C=US'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Keystore создан успешно")
                
                # Закодировать keystore в base64
                with open('temp_keystore.p12', 'rb') as f:
                    keystore_data = f.read()
                
                keystore_base64 = base64.b64encode(keystore_data).decode('utf-8')
                
                # Удалить временный файл
                os.remove('temp_keystore.p12')
                
                return {
                    'keystore': keystore_base64,
                    'storepass': keystore_password,
                    'keypass': key_password,
                    'alias': alias
                }
            else:
                print(f"❌ Ошибка создания keystore: {result.stderr}")
                return None
                
        except FileNotFoundError:
            print("❌ keytool не найден. Установите Java JDK")
            return None

def main():
    print("🚀 Enhanced APatch Build - Настройка GitHub Secrets")
    print("=" * 60)
    
    # Проверить наличие токена
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Не найден GITHUB_TOKEN в переменных окружения")
        print("💡 Установите: export GITHUB_TOKEN=your_token")
        sys.exit(1)
    
    # Определить репозиторий
    repo = "AngelOfLlife/APatch"
    
    print(f"📂 Репозиторий: {repo}")
    print(f"🔑 Токен: {'*' * (len(token)-8) + token[-8:]}")
    print()
    
    manager = EnhancedSecretsManager(token, repo)
    
    # Генерировать новый keystore
    keystore_info = manager.generate_keystore()
    if not keystore_info:
        print("❌ Не удалось создать keystore")
        sys.exit(1)
    
    # Только секреты для подписи APK
    secrets_to_add = {
        'SIGNING_KEY': keystore_info['keystore'],
        'KEY_STORE_PASSWORD': keystore_info['storepass'], 
        'KEY_PASSWORD': keystore_info['keypass'],
        'ALIAS': keystore_info['alias']
    }
    
    print("📋 Секреты для добавления:")
    print("   🔐 SIGNING_KEY - Keystore для подписи APK")
    print("   🔑 KEY_STORE_PASSWORD - Пароль keystore")
    print("   🔑 KEY_PASSWORD - Пароль ключа")
    print("   🏷️ ALIAS - Алиас ключа")
    print()
    
    # Добавить секреты
    success_count = 0
    for name, value in secrets_to_add.items():
        if manager.add_secret(name, value):
            success_count += 1
    
    print()
    print("=" * 60)
    if success_count == len(secrets_to_add):
        print("🎉 ВСЕ СЕКРЕТЫ ДОБАВЛЕНЫ УСПЕШНО!")
        print()
        print("✅ Enhanced APatch Build готов к запуску:")
        print("   • Workflow будет использовать новый keystore")
        print("   • APK будет правильно подписан")
        print("   • Проверка подписи APatch будет обойдена в коде")
        print()
        print("🚀 Теперь можно запускать workflow!")
    else:
        print(f"⚠️ Добавлено только {success_count}/{len(secrets_to_add)} секретов")
        print("❌ Проверьте права доступа и токен")

if __name__ == "__main__":
    main()