#!/usr/bin/env python3
"""
🖥️ APatch Signature Extractor for Windows 10
Быстрое извлечение подписей на Windows без зависимостей
"""

import os
import sys
import zipfile
import hashlib
import base64
import re
from pathlib import Path
import tempfile
import shutil

def print_windows_banner():
    print("🖥️ APatch Signature Extractor for Windows 10")
    print("=" * 55)
    print("Быстрое извлечение подписей без установки инструментов")
    print("=" * 55)
    print()

def check_python_version():
    """Проверяет версию Python на Windows"""
    version = sys.version_info
    print(f"🐍 Python версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("⚠️  Рекомендуется Python 3.6 или новее")
        print("📥 Скачайте с: https://www.python.org/downloads/")
    else:
        print("✅ Версия Python подходит")
    print()

def extract_signatures_windows(apk_path):
    """Windows-специфичное извлечение подписей"""
    print(f"🔍 Анализируем APK на Windows: {os.path.basename(apk_path)}")
    
    # Проверяем путь на Windows
    apk_path = os.path.abspath(apk_path)
    if not os.path.exists(apk_path):
        print(f"❌ APK файл не найден: {apk_path}")
        return None
    
    results = {
        'file_info': {},
        'package_info': {},
        'signatures': [],
        'embedded_strings': [],
        'windows_info': {}
    }
    
    # Windows-специфичная информация
    results['windows_info'] = {
        'os_name': os.name,
        'platform': sys.platform,
        'file_path': apk_path,
        'file_exists': os.path.exists(apk_path)
    }
    
    print(f"📂 Полный путь: {apk_path}")
    print(f"💻 Платформа: {sys.platform}")
    
    # Анализ файла
    print("\n📋 Анализ APK файла...")
    try:
        with open(apk_path, 'rb') as f:
            apk_content = f.read()
        
        file_size = len(apk_content)
        results['file_info'] = {
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'md5': hashlib.md5(apk_content).hexdigest(),
            'sha1': hashlib.sha1(apk_content).hexdigest(),
            'sha256': hashlib.sha256(apk_content).hexdigest(),
            'sha1_base64': base64.b64encode(hashlib.sha1(apk_content).digest()).decode(),
            'sha256_base64': base64.b64encode(hashlib.sha256(apk_content).digest()).decode()
        }
        
        print(f"  ✅ Размер: {results['file_info']['size_mb']} MB")
        print(f"  ✅ MD5: {results['file_info']['md5'][:32]}...")
        print(f"  ✅ SHA1: {results['file_info']['sha1'][:32]}...")
        
    except Exception as e:
        print(f"  ❌ Ошибка чтения файла: {e}")
        return None
    
    # Анализ содержимого APK через ZipFile
    print("\n🔍 Анализ содержимого APK...")
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            file_list = apk_zip.namelist()
            print(f"  📁 Файлов в APK: {len(file_list)}")
            
            # Анализ AndroidManifest.xml
            if 'AndroidManifest.xml' in file_list:
                manifest_content = apk_zip.read('AndroidManifest.xml')
                results['package_info'] = analyze_manifest_windows(manifest_content)
            
            # Поиск подписей в META-INF
            meta_files = [f for f in file_list if f.startswith('META-INF/')]
            print(f"  🔐 META-INF файлов: {len(meta_files)}")
            
            for meta_file in meta_files:
                if meta_file.endswith(('.RSA', '.DSA', '.EC', '.SF', '.MF')):
                    try:
                        meta_content = apk_zip.read(meta_file)
                        sig_info = analyze_meta_windows(meta_content, meta_file)
                        if sig_info:
                            results['signatures'].append(sig_info)
                            print(f"    ✅ Обработан: {meta_file}")
                    except Exception as e:
                        print(f"    ⚠️  Ошибка {meta_file}: {e}")
            
            # Поиск в .dex файлах
            dex_files = [f for f in file_list if f.endswith('.dex')]
            print(f"  📱 DEX файлов: {len(dex_files)}")
            
            for dex_file in dex_files:
                try:
                    dex_content = apk_zip.read(dex_file)
                    embedded = find_apatch_patterns_windows(dex_content, dex_file)
                    results['embedded_strings'].extend(embedded)
                except Exception as e:
                    print(f"    ⚠️  Ошибка анализа {dex_file}: {e}")
    
    except Exception as e:
        print(f"  ❌ Ошибка анализа APK: {e}")
        return None
    
    print(f"  ✅ Найдено подписей META-INF: {len(results['signatures'])}")
    print(f"  ✅ Найдено встроенных паттернов: {len(results['embedded_strings'])}")
    
    return results

def analyze_manifest_windows(manifest_content):
    """Windows-безопасный анализ манифеста"""
    info = {}
    
    try:
        # Ищем информацию о пакете в бинарном содержимом
        apatch_patterns = [
            b'me.bmax.apatch',
            b'me\.bmax\.apatch',
            b'APApplication',
            b'apatch'
        ]
        
        for pattern in apatch_patterns:
            if pattern in manifest_content:
                decoded = pattern.decode('utf-8', errors='ignore')
                if 'me.bmax.apatch' in decoded:
                    info['package_name'] = 'me.bmax.apatch'
                elif 'APApplication' in decoded:
                    info['app_class'] = 'APApplication'
        
        print(f"    📦 Пакет: {info.get('package_name', 'не найден')}")
        print(f"    🎯 Класс: {info.get('app_class', 'не найден')}")
        
    except Exception as e:
        print(f"    ⚠️  Ошибка анализа манифеста: {e}")
    
    return info

def analyze_meta_windows(content, filename):
    """Windows-безопасный анализ META-INF файлов"""
    try:
        # Вычисляем хеши содержимого
        sha1_hash = hashlib.sha1(content).digest()
        sha256_hash = hashlib.sha256(content).digest()
        md5_hash = hashlib.md5(content).digest()
        
        return {
            'file': filename,
            'size': len(content),
            'sha1_hex': sha1_hash.hex(),
            'sha1_base64': base64.b64encode(sha1_hash).decode(),
            'sha256_hex': sha256_hash.hex(),
            'sha256_base64': base64.b64encode(sha256_hash).decode(),
            'md5_hex': md5_hash.hex(),
            'md5_base64': base64.b64encode(md5_hash).decode()
        }
    except Exception as e:
        print(f"      ❌ Ошибка анализа {filename}: {e}")
        return None

def find_apatch_patterns_windows(content, filename):
    """Windows-безопасный поиск паттернов APatch"""
    patterns_found = []
    
    try:
        # Известные паттерны APatch
        apatch_signatures = [
            b'1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=',
            b'sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4=',
            b'me.bmax.apatch',
            b'APApplication',
            b'verifyAppSignature',
            b'checkSignature',
            b'verifySignature'
        ]
        
        for pattern in apatch_signatures:
            if pattern in content:
                patterns_found.append({
                    'pattern': pattern.decode('utf-8', errors='ignore'),
                    'source': filename,
                    'type': 'known_apatch_signature',
                    'found_at': filename
                })
        
        # Поиск Base64 строк
        try:
            # Пробуем декодировать как текст для поиска base64
            text_content = content.decode('utf-8', errors='ignore')
            
            # Ищем длинные base64 строки
            base64_pattern = r'[A-Za-z0-9+/]{40,}={0,2}'
            matches = re.findall(base64_pattern, text_content)
            
            for match in matches:
                if len(match) >= 40:  # Минимальная длина для подписи
                    patterns_found.append({
                        'pattern': match,
                        'source': filename,
                        'type': 'base64_candidate',
                        'length': len(match)
                    })
                    
        except:
            # Если не удается декодировать как текст, пропускаем поиск base64
            pass
            
    except Exception as e:
        print(f"      ⚠️  Ошибка поиска паттернов в {filename}: {e}")
    
    return patterns_found

def calculate_unsigned_hash_windows(apk_path):
    """Windows-специфичное вычисление хеша без подписи"""
    try:
        print("\n🔧 Вычисляем хеш APK без подписи (Windows)...")
        
        # Создаем временный файл для APK без подписи
        temp_content = bytearray()
        
        with zipfile.ZipFile(apk_path, 'r') as source_zip:
            files_without_meta = []
            for file_info in source_zip.infolist():
                if not file_info.filename.startswith('META-INF/'):
                    files_without_meta.append(file_info.filename)
                    file_content = source_zip.read(file_info.filename)
                    temp_content.extend(file_content)
            
            print(f"    📁 Файлов без META-INF: {len(files_without_meta)}")
        
        # Вычисляем хеши
        unsigned_sha1 = hashlib.sha1(temp_content).digest()
        unsigned_sha256 = hashlib.sha256(temp_content).digest()
        
        result = {
            'unsigned_sha1_hex': unsigned_sha1.hex(),
            'unsigned_sha1_base64': base64.b64encode(unsigned_sha1).decode(),
            'unsigned_sha256_hex': unsigned_sha256.hex(),
            'unsigned_sha256_base64': base64.b64encode(unsigned_sha256).decode(),
            'unsigned_size': len(temp_content)
        }
        
        print(f"    ✅ Размер без подписи: {round(len(temp_content)/(1024*1024), 2)} MB")
        print(f"    ✅ SHA1 без подписи: {result['unsigned_sha1_hex'][:32]}...")
        
        return result
        
    except Exception as e:
        print(f"    ❌ Ошибка вычисления хеша без подписи: {e}")
        return {}

def print_windows_results(results):
    """Вывод результатов для Windows"""
    print("\n" + "=" * 60)
    print("🎯 РЕЗУЛЬТАТЫ ИЗВЛЕЧЕНИЯ ПОДПИСЕЙ (Windows 10)")
    print("=" * 60)
    
    # Информация о системе
    windows_info = results.get('windows_info', {})
    print(f"\n💻 Информация о системе:")
    print(f"  • Платформа: {windows_info.get('platform', 'неизвестно')}")
    print(f"  • OS: {windows_info.get('os_name', 'неизвестно')}")
    
    # Информация о файле
    file_info = results.get('file_info', {})
    print(f"\n📱 Информация об APK:")
    print(f"  • Размер: {file_info.get('size_mb', 0)} MB")
    print(f"  • MD5: {file_info.get('md5', 'неизвестно')}")
    print(f"  • SHA1: {file_info.get('sha1', 'неизвестно')}")
    print(f"  • SHA256: {file_info.get('sha256', 'неизвестно')[:32]}...")
    
    # Информация о пакете
    package_info = results.get('package_info', {})
    print(f"\n📦 Информация о пакете:")
    print(f"  • Имя пакета: {package_info.get('package_name', 'не найдено')}")
    print(f"  • Класс приложения: {package_info.get('app_class', 'не найдено')}")
    
    # Подписи из META-INF
    signatures = results.get('signatures', [])
    print(f"\n🔐 Подписи из META-INF ({len(signatures)} файлов):")
    for i, sig in enumerate(signatures):
        print(f"  • {sig['file']}:")
        print(f"    - Размер: {sig['size']} байт")
        print(f"    - SHA1 (base64): {sig['sha1_base64']}")
        print(f"    - SHA256 (base64): {sig['sha256_base64']}")
    
    # Встроенные паттерны
    embedded = results.get('embedded_strings', [])
    apatch_patterns = [item for item in embedded if item['type'] == 'known_apatch_signature']
    base64_patterns = [item for item in embedded if item['type'] == 'base64_candidate']
    
    print(f"\n🔍 Найденные паттерны APatch ({len(apatch_patterns)}):")
    for pattern in apatch_patterns:
        print(f"  • {pattern['pattern']} (в {pattern['source']})")
    
    if base64_patterns:
        print(f"\n📝 Кандидаты на подписи ({len(base64_patterns)}):")
        for i, pattern in enumerate(base64_patterns[:5]):  # Показываем первые 5
            print(f"  • Вариант {i+1}: {pattern['pattern'][:50]}... (длина: {pattern['length']})")

def print_windows_github_secrets(results):
    """Вывод GitHub Secrets для Windows"""
    print("\n" + "=" * 65)
    print("🔑 GITHUB SECRETS ДЛЯ WINDOWS 10")
    print("=" * 65)
    
    print("\n# Скопируйте эти значения в GitHub Secrets:")
    print("# Перейдите: https://github.com/AngelOfLlife/APatch/settings/secrets/actions")
    print("# Нажмите: New repository secret")
    print()
    
    file_info = results.get('file_info', {})
    signatures = results.get('signatures', [])
    embedded = results.get('embedded_strings', [])
    
    # Варианты для APATCH_REAL_SIGNATURE
    print("# ===== APATCH_REAL_SIGNATURE =====")
    print("# Попробуйте варианты по порядку:")
    print()
    
    variant_num = 1
    
    # Вариант 1: SHA1 всего APK
    if 'sha1_base64' in file_info:
        print(f"# Вариант {variant_num} - SHA1 всего APK файла:")
        print(f"APATCH_REAL_SIGNATURE={file_info['sha1_base64']}")
        print()
        variant_num += 1
    
    # Вариант 2: SHA1 без подписи
    if 'unsigned_sha1_base64' in file_info:
        print(f"# Вариант {variant_num} - SHA1 без META-INF:")
        print(f"APATCH_REAL_SIGNATURE={file_info['unsigned_sha1_base64']}")
        print()
        variant_num += 1
    
    # Варианты 3+: из META-INF файлов
    for sig in signatures:
        print(f"# Вариант {variant_num} - SHA1 из {sig['file']}:")
        print(f"APATCH_REAL_SIGNATURE={sig['sha1_base64']}")
        print()
        variant_num += 1
        if variant_num > 6:  # Ограничиваем количество вариантов
            break
    
    # Варианты из найденных base64 строк
    base64_candidates = [item for item in embedded if item['type'] == 'base64_candidate' and len(item['pattern']) >= 40]
    for item in base64_candidates[:2]:  # Берем первые 2
        print(f"# Вариант {variant_num} - найденная base64 строка:")
        print(f"APATCH_REAL_SIGNATURE={item['pattern']}")
        print()
        variant_num += 1
    
    # CODE_SIGNATURE
    print("# ===== APATCH_CODE_SIGNATURE =====")
    if 'sha256_base64' in file_info:
        print(f"APATCH_CODE_SIGNATURE={file_info['sha256_base64']}")
    print()
    
    # Остальные секреты
    package_info = results.get('package_info', {})
    print("# ===== ОСТАЛЬНЫЕ СЕКРЕТЫ =====")
    print(f"APATCH_PACKAGE_NAME={package_info.get('package_name', 'me.bmax.apatch')}")
    print(f"APATCH_APP_CLASS={package_info.get('app_class', 'APApplication')}")
    print(f"APATCH_SIGNATURE_METHOD=verifyAppSignature")
    print()
    print("# Ключи подписи (оставьте как есть):")
    print("# SIGNING_KEY=<ваш_keystore_base64>")
    print("# ALIAS=apatch")
    print("# KEY_STORE_PASSWORD=apatch123")
    print("# KEY_PASSWORD=apatch123")

def save_results_windows(results, apk_path):
    """Сохранение результатов на Windows"""
    try:
        # Создаем имя файла результата
        apk_name = Path(apk_path).stem
        timestamp = hashlib.md5(str(apk_path).encode()).hexdigest()[:8]
        output_file = f"apatch_signatures_{apk_name}_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("APatch Signature Extraction Results (Windows 10)\n")
            f.write("=" * 50 + "\n\n")
            
            # Основная информация
            file_info = results.get('file_info', {})
            f.write(f"APK файл: {os.path.basename(apk_path)}\n")
            f.write(f"Размер: {file_info.get('size_mb', 0)} MB\n")
            f.write(f"SHA1: {file_info.get('sha1', 'неизвестно')}\n")
            f.write(f"SHA256: {file_info.get('sha256', 'неизвестно')}\n\n")
            
            # GitHub Secrets
            f.write("ОСНОВНЫЕ GITHUB SECRETS:\n")
            f.write("=" * 30 + "\n")
            f.write(f"APATCH_REAL_SIGNATURE={file_info.get('sha1_base64', '')}\n")
            f.write(f"APATCH_CODE_SIGNATURE={file_info.get('sha256_base64', '')}\n")
            
            package_info = results.get('package_info', {})
            f.write(f"APATCH_PACKAGE_NAME={package_info.get('package_name', 'me.bmax.apatch')}\n")
            f.write(f"APATCH_APP_CLASS={package_info.get('app_class', 'APApplication')}\n")
            f.write(f"APATCH_SIGNATURE_METHOD=verifyAppSignature\n\n")
            
            # Альтернативные варианты
            signatures = results.get('signatures', [])
            if signatures:
                f.write("АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ:\n")
                f.write("=" * 30 + "\n")
                for i, sig in enumerate(signatures):
                    f.write(f"Вариант {i+2} ({sig['file']}): {sig['sha1_base64']}\n")
        
        print(f"\n💾 Результаты сохранены в файл: {output_file}")
        print(f"📂 Полный путь: {os.path.abspath(output_file)}")
        
        return output_file
        
    except Exception as e:
        print(f"\n⚠️  Ошибка сохранения файла: {e}")
        return None

def main():
    print_windows_banner()
    check_python_version()
    
    if len(sys.argv) != 2:
        print("❌ Использование:")
        print("   python windows_quick_extract.py <путь_к_apk>")
        print()
        print("📝 Примеры:")
        print("   python windows_quick_extract.py APatch.apk")
        print("   python windows_quick_extract.py C:\\Downloads\\APatch-11107-release.apk")
        print("   python windows_quick_extract.py \"C:\\Мои файлы\\APatch.apk\"")
        print()
        print("💡 Советы для Windows:")
        print("   • Используйте кавычки если в пути есть пробелы")
        print("   • Можете перетащить APK файл на этот скрипт")
        print("   • Путь должен содержать расширение .apk")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    
    # Windows-специфичная обработка путей
    apk_path = os.path.normpath(apk_path)
    
    if not os.path.exists(apk_path):
        print(f"❌ APK файл не найден: {apk_path}")
        print()
        print("🔍 Проверьте:")
        print("   • Правильность пути к файлу")
        print("   • Существование файла")
        print("   • Права доступа к файлу")
        sys.exit(1)
    
    if not apk_path.lower().endswith('.apk'):
        print(f"⚠️  Внимание: файл не имеет расширения .apk")
        print(f"   Файл: {apk_path}")
        response = input("Продолжить анализ? (y/n): ")
        if response.lower() not in ['y', 'yes', 'да', 'д']:
            sys.exit(0)
    
    try:
        print(f"🚀 Начинаем анализ APK на Windows 10...")
        print(f"📁 Файл: {os.path.basename(apk_path)}")
        print(f"📂 Путь: {apk_path}")
        
        # Извлекаем подписи
        results = extract_signatures_windows(apk_path)
        
        if not results:
            print("\n❌ Не удалось извлечь подписи из APK")
            sys.exit(1)
        
        # Добавляем хеш без подписи
        unsigned_hash = calculate_unsigned_hash_windows(apk_path)
        results['file_info'].update(unsigned_hash)
        
        # Выводим результаты
        print_windows_results(results)
        print_windows_github_secrets(results)
        
        # Сохраняем результаты
        output_file = save_results_windows(results, apk_path)
        
        print("\n" + "=" * 60)
        print("🎉 АНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")
        print("=" * 60)
        print()
        print("📋 Что делать дальше:")
        print("1. Скопируйте найденные APATCH_REAL_SIGNATURE и APATCH_CODE_SIGNATURE")
        print("2. Перейдите: https://github.com/AngelOfLlife/APatch/settings/secrets/actions")
        print("3. Обновите секреты с новыми значениями")
        print("4. Запустите GitHub Actions workflow")
        print("5. Скачайте готовый APK без зависания!")
        print()
        print("💡 Если первый вариант подписи не сработает, попробуйте следующие варианты!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Анализ прерван пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("\n🆘 Попробуйте:")
        print("   • Запустить от имени администратора")
        print("   • Проверить целостность APK файла")
        print("   • Использовать путь без пробелов и спецсимволов")
        sys.exit(1)

if __name__ == "__main__":
    main()