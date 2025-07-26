#!/usr/bin/env python3
"""
Умный генератор keystore с различными стратегиями поиска
"""

import subprocess
import os
import base64
import hashlib
import time
import threading
import random
import string
from multiprocessing import Pool, Manager, Value
from datetime import datetime

# Целевые отпечатки
TARGETS = {
    "APATCH_CODE_SIGNATURE": "1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=",
    "APATCH_REAL_SIGNATURE": "sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4="
}

class KeystoreGenerator:
    def __init__(self):
        self.attempts = Value('i', 0)
        self.start_time = time.time()
        self.found = Value('b', False)
        self.best_matches = Manager().dict()
        
    def generate_random_string(self, length=10):
        """Генерирует случайную строку"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def create_keystore_variations(self, base_name="APatch"):
        """Создает различные вариации имени и параметров"""
        variations = [
            # Базовые варианты
            f"CN={base_name}, OU=Android, O=APatch, L=Unknown, S=Unknown, C=US",
            f"CN={base_name}, OU=Dev, O=APatch, L=Beijing, S=Beijing, C=CN",
            f"CN={base_name}, OU=Team, O=APatch, L=Shanghai, S=Shanghai, C=CN",
            
            # Вариации с номерами
            f"CN={base_name}_Dev, OU=Development, O=APatch, L=Test, S=Test, C=US",
            f"CN={base_name}_Release, OU=Release, O=APatch, L=Prod, S=Prod, C=US",
            
            # Случайные вариации
            f"CN={self.generate_random_string()}, OU={self.generate_random_string()}, O=APatch, L=City, S=State, C=US",
        ]
        return variations
    
    def generate_keystore_with_params(self, dname, keysize=2048, algorithm="RSA"):
        """Генерирует keystore с заданными параметрами"""
        with self.attempts.get_lock():
            self.attempts.value += 1
            
        if self.found.value:
            return None
            
        attempt_id = self.generate_random_string(8)
        alias = f"apatch_{attempt_id}"
        keystore_name = f"temp_{attempt_id}.p12"
        password = f"pass_{attempt_id}"
        
        try:
            # Генерируем keystore
            cmd = [
                "keytool", "-genkeypair", "-v",
                "-keystore", keystore_name,
                "-storetype", "PKCS12",
                "-alias", alias,
                "-keyalg", algorithm,
                "-keysize", str(keysize),
                "-validity", "10000",
                "-storepass", password,
                "-keypass", password,
                "-dname", dname
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return None
                
            # Получаем отпечаток
            cmd_fingerprint = [
                "keytool", "-list", "-v",
                "-keystore", keystore_name,
                "-storetype", "PKCS12",
                "-storepass", password,
                "-alias", alias
            ]
            
            result_fp = subprocess.run(cmd_fingerprint, capture_output=True, text=True, timeout=30)
            
            if result_fp.returncode != 0:
                return None
                
            # Анализируем результат
            return self.analyze_fingerprint(result_fp.stdout, keystore_name, alias, password, dname)
            
        except Exception as e:
            return None
        finally:
            try:
                os.remove(keystore_name)
            except:
                pass
                
    def analyze_fingerprint(self, keytool_output, keystore_name, alias, password, dname):
        """Анализирует отпечаток и ищет совпадения"""
        lines = keytool_output.split('\n')
        
        for line in lines:
            if 'SHA256:' in line:
                try:
                    hex_part = line.split('SHA256:')[1].strip()
                    hex_clean = hex_part.replace(':', '').replace(' ', '').upper()
                    fingerprint_bytes = bytes.fromhex(hex_clean)
                    fingerprint_b64 = base64.b64encode(fingerprint_bytes).decode()
                    
                    # Проверяем все целевые отпечатки
                    for target_name, target_fp in TARGETS.items():
                        if fingerprint_b64 == target_fp:
                            print(f"🎉 НАЙДЕН ТОЧНЫЙ КЛЮЧ ДЛЯ {target_name}!")
                            self.save_found_key(keystore_name, alias, password, fingerprint_b64, target_name, dname)
                            self.found.value = True
                            return True
                            
                        # Проверяем частичные совпадения
                        for prefix_len in [4, 8, 12, 16, 20]:
                            if fingerprint_b64[:prefix_len] == target_fp[:prefix_len]:
                                match_key = f"{target_name}_{prefix_len}"
                                if match_key not in self.best_matches or len(self.best_matches[match_key]['fp']) < len(fingerprint_b64):
                                    self.best_matches[match_key] = {
                                        'fp': fingerprint_b64,
                                        'keystore': keystore_name,
                                        'alias': alias,
                                        'password': password,
                                        'dname': dname,
                                        'prefix_len': prefix_len
                                    }
                                    print(f"🎯 Новое лучшее частичное совпадение {target_name} ({prefix_len} символов): {fingerprint_b64[:prefix_len]}...")
                    
                    return False
                    
                except Exception as e:
                    pass
                    
        return False
    
    def save_found_key(self, keystore_name, alias, password, fingerprint, target_name, dname):
        """Сохраняет найденный ключ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FOUND_KEY_{target_name}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"🎉 НАЙДЕН ТОЧНЫЙ КЛЮЧ ДЛЯ {target_name}!\n")
            f.write(f"Файл: {keystore_name}\n")
            f.write(f"Алиас: {alias}\n")
            f.write(f"Пароль: {password}\n")
            f.write(f"Отпечаток: {fingerprint}\n")
            f.write(f"DN: {dname}\n")
            f.write(f"Попыток потребовалось: {self.attempts.value}\n")
            f.write(f"Время: {time.time() - self.start_time:.1f} секунд\n")
        
        print(f"💾 Информация сохранена в {filename}")
    
    def worker_process(self, process_id):
        """Рабочий процесс для параллельной генерации"""
        while not self.found.value:
            try:
                # Выбираем случайные параметры
                dname_variations = self.create_keystore_variations()
                dname = random.choice(dname_variations)
                keysize = random.choice([2048, 3072, 4096])  # Различные размеры ключей
                algorithm = random.choice(["RSA", "EC"])      # Различные алгоритмы
                
                self.generate_keystore_with_params(dname, keysize, algorithm)
                
            except Exception as e:
                continue
    
    def print_stats(self):
        """Печать статистики"""
        while not self.found.value:
            time.sleep(15)
            elapsed = time.time() - self.start_time
            rate = self.attempts.value / elapsed if elapsed > 0 else 0
            
            print(f"📊 Статистика:")
            print(f"   Попыток: {self.attempts.value:,}")
            print(f"   Скорость: {rate:.1f}/сек")
            print(f"   Время: {elapsed:.1f}сек")
            print(f"   Лучших совпадений: {len(self.best_matches)}")
            print("=" * 40)
    
    def run_parallel_search(self, num_processes=4, max_attempts=100000):
        """Запуск параллельного поиска"""
        print("🔑 Умный генератор keystore")
        print("=" * 50)
        for name, fp in TARGETS.items():
            print(f"🎯 {name}: {fp}")
        print("=" * 50)
        print(f"🚀 Запуск {num_processes} параллельных процессов")
        print(f"⏱️  Максимум попыток: {max_attempts:,}")
        print("💡 Нажмите Ctrl+C для остановки")
        print("=" * 50)
        
        # Проверяем keytool
        try:
            subprocess.run(["keytool", "-help"], capture_output=True, timeout=5)
        except:
            print("❌ keytool не найден! Установите Java JDK")
            return
        
        # Запуск статистики
        stats_thread = threading.Thread(target=self.print_stats, daemon=True)
        stats_thread.start()
        
        try:
            # Запуск рабочих процессов
            with Pool(num_processes) as pool:
                results = []
                for i in range(num_processes):
                    result = pool.apply_async(self.worker_process, (i,))
                    results.append(result)
                
                # Ждем завершения или достижения лимита
                while not self.found.value and self.attempts.value < max_attempts:
                    time.sleep(1)
                
                if self.attempts.value >= max_attempts:
                    print(f"\n⏹️  Достигнут лимит попыток: {max_attempts:,}")
                
                # Завершаем процессы
                pool.terminate()
                pool.join()
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Остановлено пользователем")
        
        self.show_final_results()
    
    def show_final_results(self):
        """Показывает финальные результаты"""
        elapsed = time.time() - self.start_time
        
        print(f"\n📊 ФИНАЛЬНАЯ СТАТИСТИКА:")
        print(f"   Попыток: {self.attempts.value:,}")
        print(f"   Время: {elapsed:.1f} секунд")
        print(f"   Скорость: {self.attempts.value/elapsed:.1f} попыток/сек")
        
        if self.best_matches:
            print(f"\n🎯 ЛУЧШИЕ ЧАСТИЧНЫЕ СОВПАДЕНИЯ:")
            for match_key, match_data in sorted(self.best_matches.items(), 
                                               key=lambda x: x[1]['prefix_len'], reverse=True):
                print(f"   {match_key}: {match_data['fp'][:match_data['prefix_len']]}... ({match_data['prefix_len']} символов)")
        
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        print(f"   1. Используйте enhanced_apatch_build.yml для обхода проверки подписи")
        print(f"   2. Поищите оригинальный SIGNING_KEY у разработчиков")
        print(f"   3. Рассмотрите альтернативные Xposed фреймворки")

def main():
    generator = KeystoreGenerator()
    
    # Настройки поиска
    num_processes = min(4, os.cpu_count() or 1)  # Не больше 4 процессов
    max_attempts = 50000  # Ограничение для демонстрации
    
    generator.run_parallel_search(num_processes, max_attempts)

if __name__ == "__main__":
    main()