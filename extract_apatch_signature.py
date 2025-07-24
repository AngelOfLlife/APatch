#!/usr/bin/env python3
"""
APatch Signature Extractor
Извлекает подпись из APK файла в формате, который использует APatch для проверки
"""

import zipfile
import hashlib
import base64
import sys
import os

def extract_apatch_signature(apk_path):
    """
    Извлекает подпись в формате, который использует APatch
    Возвращает Base64-кодированный SHA256 хеш сертификата
    """
    
    if not os.path.exists(apk_path):
        print(f"Файл {apk_path} не найден")
        return None
        
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk:
            # Найти файлы сертификатов в META-INF
            cert_files = []
            for file_name in apk.namelist():
                if file_name.startswith('META-INF/') and (file_name.endswith('.RSA') or file_name.endswith('.DSA')):
                    cert_files.append(file_name)
            
            if not cert_files:
                print("Файлы сертификатов не найдены в APK")
                return None
                
            print(f"Найдены файлы сертификатов: {cert_files}")
            
            # Берем первый найденный сертификат
            cert_file = cert_files[0]
            cert_data = apk.read(cert_file)
            
            print(f"Извлекаем сертификат из: {cert_file}")
            print(f"Размер данных сертификата: {len(cert_data)} байт")
            
            # Для APatch используется простой SHA256 хеш данных сертификата
            # (не DER-кодированного X.509, а самих сырых данных)
            sha256_hash = hashlib.sha256(cert_data).digest()
            
            # Конвертируем в Base64
            signature_base64 = base64.b64encode(sha256_hash).decode('utf-8')
            
            return signature_base64
            
    except zipfile.BadZipFile:
        print("Ошибка: файл не является корректным APK/ZIP архивом")
        return None
    except Exception as e:
        print(f"Ошибка при обработке APK: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Использование: python3 extract_apatch_signature.py <путь_к_apk>")
        print("Пример: python3 extract_apatch_signature.py app-release.apk")
        sys.exit(1)
        
    apk_path = sys.argv[1]
    print(f"Извлечение подписи из: {apk_path}")
    print("-" * 50)
    
    signature = extract_apatch_signature(apk_path)
    
    if signature:
        print("-" * 50)
        print("✅ Подпись успешно извлечена!")
        print(f"APatch signature: {signature}")
        print("-" * 50)
        print("Для использования в коде замените в файле APatchApp.kt:")
        print(f'verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")')
        print("на:")
        print(f'verifyAppSignature("{signature}")')
        print("-" * 50)
        
        # Сохранить в файл для удобства
        with open('apatch_signature.txt', 'w') as f:
            f.write(signature)
        print("💾 Подпись сохранена в файл: apatch_signature.txt")
        
    else:
        print("❌ Не удалось извлечь подпись")
        sys.exit(1)

if __name__ == "__main__":
    main()