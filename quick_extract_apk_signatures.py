#!/usr/bin/env python3
"""
⚡ Quick APatch Signature Extractor
Быстрое извлечение подписей без внешних зависимостей
"""

import os
import sys
import zipfile
import hashlib
import base64
import re
from pathlib import Path

def extract_signatures_quick(apk_path):
    """Быстро извлекает основные подписи из APK"""
    print(f"⚡ Быстрый анализ APK: {apk_path}")
    
    results = {
        'file_info': {},
        'package_info': {},
        'signatures': [],
        'embedded_strings': []
    }
    
    # 1. Информация о файле
    print("\n📋 Анализ файла...")
    with open(apk_path, 'rb') as f:
        apk_content = f.read()
    
    results['file_info'] = {
        'size_mb': round(len(apk_content) / (1024 * 1024), 2),
        'md5': hashlib.md5(apk_content).hexdigest(),
        'sha1': hashlib.sha1(apk_content).hexdigest(),
        'sha256': hashlib.sha256(apk_content).hexdigest(),
        'sha1_base64': base64.b64encode(hashlib.sha1(apk_content).digest()).decode(),
        'sha256_base64': base64.b64encode(hashlib.sha256(apk_content).digest()).decode()
    }
    
    print(f"  ✅ Размер: {results['file_info']['size_mb']} MB")
    print(f"  ✅ SHA1: {results['file_info']['sha1'][:32]}...")
    
    # 2. Анализ содержимого APK
    print("\n🔍 Анализ содержимого APK...")
    with zipfile.ZipFile(apk_path, 'r') as apk_zip:
        # Извлекаем AndroidManifest.xml
        if 'AndroidManifest.xml' in apk_zip.namelist():
            manifest_content = apk_zip.read('AndroidManifest.xml')
            results['package_info'] = extract_package_from_manifest(manifest_content)
        
        # Ищем подписи в META-INF
        meta_files = [f for f in apk_zip.namelist() if f.startswith('META-INF/')]
        for meta_file in meta_files:
            if meta_file.endswith(('.RSA', '.DSA', '.EC', '.SF', '.MF')):
                try:
                    meta_content = apk_zip.read(meta_file)
                    sig_info = analyze_meta_file(meta_content, meta_file)
                    if sig_info:
                        results['signatures'].append(sig_info)
                except:
                    pass
        
        # Ищем встроенные строки в .dex файлах
        dex_files = [f for f in apk_zip.namelist() if f.endswith('.dex')]
        for dex_file in dex_files:
            try:
                dex_content = apk_zip.read(dex_file)
                embedded = find_embedded_strings(dex_content, dex_file)
                results['embedded_strings'].extend(embedded)
            except:
                pass
    
    print(f"  ✅ Найдено подписей в META-INF: {len(results['signatures'])}")
    print(f"  ✅ Найдено встроенных строк: {len(results['embedded_strings'])}")
    
    return results

def extract_package_from_manifest(manifest_content):
    """Извлекает информацию о пакете из манифеста"""
    info = {}
    
    try:
        # Ищем в бинарном содержимом
        text_content = manifest_content.decode('utf-8', errors='ignore')
        
        # Ищем имя пакета
        package_patterns = [
            rb'me\.bmax\.apatch',
            rb'me.bmax.apatch',
            b'me.bmax.apatch'
        ]
        
        for pattern in package_patterns:
            if pattern in manifest_content:
                info['package_name'] = pattern.decode('utf-8', errors='ignore')
                break
        
        # Ищем APApplication
        if b'APApplication' in manifest_content:
            info['app_class'] = 'APApplication'
        
        print(f"  ✅ Пакет: {info.get('package_name', 'не найден')}")
        
    except Exception as e:
        print(f"  ⚠️  Ошибка анализа манифеста: {e}")
    
    return info

def analyze_meta_file(content, filename):
    """Анализирует файлы META-INF"""
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
    except:
        return None

def find_embedded_strings(content, filename):
    """Ищет встроенные строки в бинарном содержимом"""
    strings = []
    
    try:
        # Известные паттерны APatch
        apatch_patterns = [
            b'1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=',
            b'sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4=',
            b'me.bmax.apatch',
            b'APApplication',
            b'verifyAppSignature',
            b'checkSignature',
            b'verifySignature',
            b'validateSignature'
        ]
        
        for pattern in apatch_patterns:
            if pattern in content:
                strings.append({
                    'pattern': pattern.decode('utf-8', errors='ignore'),
                    'source': filename,
                    'type': 'known_apatch_pattern'
                })
        
        # Ищем base64 строки (длинные)
        try:
            text_content = content.decode('utf-8', errors='ignore')
            base64_matches = re.findall(r'[A-Za-z0-9+/]{40,}={0,2}', text_content)
            for match in base64_matches:
                if len(match) >= 40:  # Минимальная длина для подписи
                    strings.append({
                        'pattern': match,
                        'source': filename,
                        'type': 'base64_candidate',
                        'length': len(match)
                    })
        except:
            pass
        
    except Exception as e:
        pass
    
    return strings

def calculate_unsigned_hash(apk_path):
    """Вычисляет хеш APK без подписи"""
    try:
        print("\n🔧 Вычисляем хеш без подписи...")
        
        # Создаем временный APK без META-INF
        temp_content = bytearray()
        
        with zipfile.ZipFile(apk_path, 'r') as source_zip:
            for file_info in source_zip.infolist():
                if not file_info.filename.startswith('META-INF/'):
                    file_content = source_zip.read(file_info.filename)
                    temp_content.extend(file_content)
        
        # Вычисляем хеши
        unsigned_sha1 = hashlib.sha1(temp_content).digest()
        unsigned_sha256 = hashlib.sha256(temp_content).digest()
        
        result = {
            'unsigned_sha1_hex': unsigned_sha1.hex(),
            'unsigned_sha1_base64': base64.b64encode(unsigned_sha1).decode(),
            'unsigned_sha256_hex': unsigned_sha256.hex(),
            'unsigned_sha256_base64': base64.b64encode(unsigned_sha256).decode()
        }
        
        print(f"  ✅ Хеш без подписи вычислен")
        return result
        
    except Exception as e:
        print(f"  ❌ Ошибка вычисления хеша без подписи: {e}")
        return {}

def print_results(results):
    """Выводит результаты в удобном формате"""
    print("\n" + "=" * 60)
    print("🎯 РЕЗУЛЬТАТЫ ИЗВЛЕЧЕНИЯ ПОДПИСЕЙ")
    print("=" * 60)
    
    # Информация о файле
    file_info = results['file_info']
    print(f"\n📱 Информация о файле:")
    print(f"  • Размер: {file_info['size_mb']} MB")
    print(f"  • MD5: {file_info['md5']}")
    print(f"  • SHA1: {file_info['sha1']}")
    print(f"  • SHA256: {file_info['sha256'][:32]}...")
    
    # Информация о пакете
    package_info = results['package_info']
    print(f"\n📦 Информация о пакете:")
    print(f"  • Имя пакета: {package_info.get('package_name', 'не найдено')}")
    print(f"  • Класс приложения: {package_info.get('app_class', 'не найдено')}")
    
    # Подписи из META-INF
    signatures = results['signatures']
    print(f"\n🔐 Подписи из META-INF ({len(signatures)} файлов):")
    for sig in signatures:
        print(f"  • {sig['file']}:")
        print(f"    - SHA1 (base64): {sig['sha1_base64']}")
        print(f"    - SHA256 (base64): {sig['sha256_base64']}")
    
    # Встроенные строки
    embedded = results['embedded_strings']
    print(f"\n🔍 Найденные встроенные строки ({len(embedded)}):")
    for item in embedded:
        if item['type'] == 'known_apatch_pattern':
            print(f"  • {item['pattern']} (из {item['source']})")
    
    # Кандидаты на подписи
    base64_candidates = [item for item in embedded if item['type'] == 'base64_candidate']
    if base64_candidates:
        print(f"\n📝 Кандидаты на подписи (base64, {len(base64_candidates)} найдено):")
        for item in base64_candidates[:5]:  # Показываем первые 5
            print(f"  • {item['pattern'][:50]}... (длина: {item['length']})")

def print_github_secrets(results):
    """Выводит результаты в формате GitHub Secrets"""
    print("\n" + "=" * 60)
    print("🔑 СЕКРЕТЫ ДЛЯ GITHUB ACTIONS")
    print("=" * 60)
    
    print("\n# Скопируйте эти значения в GitHub Secrets:")
    print("# Repository → Settings → Secrets and variables → Actions")
    print()
    
    # Основные кандидаты на подписи
    file_info = results['file_info']
    signatures = results['signatures']
    embedded = results['embedded_strings']
    
    # Варианты для APATCH_REAL_SIGNATURE
    print("# APATCH_REAL_SIGNATURE (попробуйте варианты по порядку):")
    
    variant = 1
    
    # Из файла целиком
    print(f"# Вариант {variant} (SHA1 всего APK):")
    print(f"APATCH_REAL_SIGNATURE={file_info['sha1_base64']}")
    variant += 1
    
    # Из подписей META-INF
    for sig in signatures:
        print(f"# Вариант {variant} (SHA1 из {sig['file']}):")
        print(f"APATCH_REAL_SIGNATURE={sig['sha1_base64']}")
        variant += 1
        if variant > 5:  # Ограничиваем количество вариантов
            break
    
    # Из встроенных base64 строк
    base64_candidates = [item for item in embedded if item['type'] == 'base64_candidate' and len(item['pattern']) >= 40]
    for item in base64_candidates[:3]:
        print(f"# Вариант {variant} (найденная base64 строка):")
        print(f"APATCH_REAL_SIGNATURE={item['pattern']}")
        variant += 1
    
    print(f"\n# APATCH_CODE_SIGNATURE (используйте те же варианты):")
    print(f"APATCH_CODE_SIGNATURE={file_info['sha256_base64']}")
    
    # Информация о пакете
    package_info = results['package_info']
    print(f"\n# Информация о пакете:")
    print(f"APATCH_PACKAGE_NAME={package_info.get('package_name', 'me.bmax.apatch')}")
    print(f"APATCH_APP_CLASS={package_info.get('app_class', 'APApplication')}")
    print(f"APATCH_SIGNATURE_METHOD=verifyAppSignature")

def main():
    print("⚡ Quick APatch Signature Extractor")
    print("=" * 50)
    
    if len(sys.argv) != 2:
        print("❌ Использование: python3 quick_extract_apk_signatures.py <апк_файл>")
        print("\nПример:")
        print("  python3 quick_extract_apk_signatures.py APatch-11107-release.apk")
        print("\nЭтот скрипт НЕ требует внешних зависимостей!")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    
    if not os.path.exists(apk_path):
        print(f"❌ APK файл не найден: {apk_path}")
        sys.exit(1)
    
    try:
        # Извлекаем подписи
        results = extract_signatures_quick(apk_path)
        
        # Добавляем хеш без подписи
        unsigned_hash = calculate_unsigned_hash(apk_path)
        results['file_info'].update(unsigned_hash)
        
        # Выводим результаты
        print_results(results)
        print_github_secrets(results)
        
        # Сохраняем в файл
        output_file = f"quick_signatures_{Path(apk_path).stem}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("APatch Signature Extraction Results\n")
            f.write("=" * 40 + "\n\n")
            
            f.write(f"File: {apk_path}\n")
            f.write(f"Size: {results['file_info']['size_mb']} MB\n")
            f.write(f"SHA1: {results['file_info']['sha1']}\n")
            f.write(f"SHA256: {results['file_info']['sha256']}\n\n")
            
            f.write("GitHub Secrets:\n")
            f.write(f"APATCH_REAL_SIGNATURE={results['file_info']['sha1_base64']}\n")
            f.write(f"APATCH_CODE_SIGNATURE={results['file_info']['sha256_base64']}\n")
            
            package_info = results['package_info']
            f.write(f"APATCH_PACKAGE_NAME={package_info.get('package_name', 'me.bmax.apatch')}\n")
            f.write(f"APATCH_APP_CLASS={package_info.get('app_class', 'APApplication')}\n")
            f.write(f"APATCH_SIGNATURE_METHOD=verifyAppSignature\n")
        
        print(f"\n💾 Результаты также сохранены в файл: {output_file}")
        print(f"\n🎉 Извлечение завершено! Используйте найденные подписи в GitHub Secrets.")
        
    except Exception as e:
        print(f"\n❌ Ошибка извлечения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()