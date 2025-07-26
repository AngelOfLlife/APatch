#!/usr/bin/env python3
"""
Скрипт для попытки генерации keystore с определенным SHA-256 отпечатком
ВНИМАНИЕ: Это может занять ОЧЕНЬ много времени (теоретически бесконечно)
"""

import subprocess
import os
import base64
import hashlib
import time
import threading
from datetime import datetime

# Целевой отпечаток (который мы хотим получить)
TARGET_FINGERPRINT = "1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
TARGET_BYTES = base64.b64decode(TARGET_FINGERPRINT)
TARGET_HEX = TARGET_BYTES.hex()

# Счетчики
attempts = 0
start_time = time.time()
found = False

def print_stats():
    """Печать статистики каждые 10 секунд"""
    global attempts, start_time
    while not found:
        time.sleep(10)
        elapsed = time.time() - start_time
        rate = attempts / elapsed if elapsed > 0 else 0
        print(f"📊 Попыток: {attempts:,} | Скорость: {rate:.1f}/сек | Время: {elapsed:.1f}сек")

def generate_keystore(attempt_num):
    """Генерирует keystore и проверяет отпечаток"""
    global attempts, found
    
    if found:
        return None
        
    attempts += 1
    
    # Генерируем случайные параметры
    alias = f"apatch_{attempt_num}"
    keystore_name = f"temp_keystore_{attempt_num}.p12"
    password = f"temp_pass_{attempt_num}"
    
    try:
        # Генерируем keystore
        cmd = [
            "keytool", "-genkeypair",
            "-v",
            "-keystore", keystore_name,
            "-storetype", "PKCS12",
            "-alias", alias,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", password,
            "-keypass", password,
            "-dname", f"CN=APatch_{attempt_num}, OU=Test, O=Test, L=Test, S=Test, C=US"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return None
            
        # Получаем отпечаток
        cmd_fingerprint = [
            "keytool", "-list",
            "-v",
            "-keystore", keystore_name,
            "-storetype", "PKCS12",
            "-storepass", password,
            "-alias", alias
        ]
        
        result_fp = subprocess.run(cmd_fingerprint, capture_output=True, text=True, timeout=30)
        
        if result_fp.returncode != 0:
            return None
            
        # Ищем SHA256 отпечаток в выводе
        lines = result_fp.stdout.split('\n')
        for line in lines:
            if 'SHA256:' in line:
                # Извлекаем hex значение
                hex_part = line.split('SHA256:')[1].strip()
                hex_clean = hex_part.replace(':', '').replace(' ', '').upper()
                
                # Конвертируем в base64 для сравнения
                try:
                    fingerprint_bytes = bytes.fromhex(hex_clean)
                    fingerprint_b64 = base64.b64encode(fingerprint_bytes).decode()
                    
                    print(f"🔍 Попытка {attempt_num}: {fingerprint_b64}")
                    
                    # Проверяем совпадение
                    if fingerprint_b64 == TARGET_FINGERPRINT:
                        print(f"🎉 НАЙДЕН СОВПАДАЮЩИЙ КЛЮЧ!")
                        print(f"📁 Файл: {keystore_name}")
                        print(f"🔑 Алиас: {alias}")
                        print(f"🔒 Пароль: {password}")
                        print(f"📋 Отпечаток: {fingerprint_b64}")
                        
                        # Сохраняем информацию
                        with open("FOUND_KEYSTORE_INFO.txt", "w") as f:
                            f.write(f"НАЙДЕН СОВПАДАЮЩИЙ КЛЮЧ!\n")
                            f.write(f"Файл: {keystore_name}\n")
                            f.write(f"Алиас: {alias}\n")
                            f.write(f"Пароль: {password}\n")
                            f.write(f"Отпечаток: {fingerprint_b64}\n")
                            f.write(f"Попыток потребовалось: {attempt_num}\n")
                            f.write(f"Время: {time.time() - start_time:.1f} секунд\n")
                        
                        found = True
                        return {
                            'keystore': keystore_name,
                            'alias': alias,
                            'password': password,
                            'fingerprint': fingerprint_b64
                        }
                        
                    # Проверяем частичные совпадения (первые N символов)
                    for prefix_len in [8, 12, 16, 20]:
                        if fingerprint_b64[:prefix_len] == TARGET_FINGERPRINT[:prefix_len]:
                            print(f"🎯 ЧАСТИЧНОЕ СОВПАДЕНИЕ ({prefix_len} символов): {fingerprint_b64}")
                            with open("PARTIAL_MATCHES.txt", "a") as f:
                                f.write(f"Попытка {attempt_num}: {fingerprint_b64} (совпадение {prefix_len} символов)\n")
                            
                except Exception as e:
                    pass
                    
                break
                
    except Exception as e:
        pass
    finally:
        # Удаляем временный keystore
        try:
            os.remove(keystore_name)
        except:
            pass
            
    return None

def main():
    """Основная функция"""
    global found
    
    print("🔑 Генератор keystore с целевым отпечатком")
    print("=" * 50)
    print(f"🎯 Целевой отпечаток: {TARGET_FINGERPRINT}")
    print(f"🎯 Целевой HEX: {TARGET_HEX}")
    print("=" * 50)
    print("⚠️  ВНИМАНИЕ: Это может занять ОЧЕНЬ много времени!")
    print("⚠️  SHA-256 collision практически невозможен с современными технологиями")
    print("⚠️  Рекомендуется прервать через несколько минут и использовать другие методы")
    print("=" * 50)
    
    # Запуск статистики в отдельном потоке
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()
    
    # Проверяем наличие keytool
    try:
        subprocess.run(["keytool", "-help"], capture_output=True, timeout=5)
    except:
        print("❌ keytool не найден! Установите Java JDK")
        return
        
    print("🚀 Начинаем генерацию ключей...")
    print("💡 Нажмите Ctrl+C для остановки")
    
    try:
        attempt = 1
        while not found:
            result = generate_keystore(attempt)
            if result:
                break
            attempt += 1
            
            # Ограничиваем количество попыток для демонстрации
            if attempt > 10000:  # Остановка после 10K попыток
                print(f"\n⏹️  Остановлено после {attempt-1} попыток")
                print("💡 Для продолжения увеличьте лимит в коде")
                break
                
    except KeyboardInterrupt:
        print(f"\n⏹️  Остановлено пользователем после {attempts} попыток")
        
    elapsed = time.time() - start_time
    print(f"📊 Финальная статистика:")
    print(f"   Попыток: {attempts:,}")
    print(f"   Время: {elapsed:.1f} секунд")
    print(f"   Скорость: {attempts/elapsed:.1f} попыток/сек")
    
    if os.path.exists("PARTIAL_MATCHES.txt"):
        print(f"📋 Частичные совпадения сохранены в PARTIAL_MATCHES.txt")

if __name__ == "__main__":
    main()