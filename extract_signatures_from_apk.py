#!/usr/bin/env python3
"""
🔍 APatch Signature Extractor
Извлекает все подписи и метаданные из оригинального APK APatch
"""

import os
import sys
import zipfile
import hashlib
import base64
import subprocess
import tempfile
import shutil
import re
from pathlib import Path

def print_banner():
    print("🔍 APatch Signature Extractor v2.0")
    print("=" * 50)
    print("Извлекает подписи из оригинального APK APatch")
    print("=" * 50)
    print()

def extract_apk_signatures(apk_path):
    """Извлекает все возможные подписи из APK"""
    print(f"📱 Анализируем APK: {apk_path}")
    
    if not os.path.exists(apk_path):
        print(f"❌ APK файл не найден: {apk_path}")
        return None
    
    results = {
        'apk_info': {},
        'cert_signatures': [],
        'embedded_signatures': [],
        'code_signatures': [],
        'package_info': {},
        'hash_signatures': []
    }
    
    # 1. Основная информация об APK
    print("\n📋 Извлекаем основную информацию...")
    results['apk_info'] = get_apk_basic_info(apk_path)
    
    # 2. Подписи сертификатов
    print("\n🔐 Извлекаем подписи сертификатов...")
    results['cert_signatures'] = extract_certificate_signatures(apk_path)
    
    # 3. Встроенные подписи в коде
    print("\n🔍 Ищем встроенные подписи в коде...")
    results['embedded_signatures'] = extract_embedded_signatures(apk_path)
    
    # 4. Хеши и контрольные суммы
    print("\n🔧 Вычисляем хеши и контрольные суммы...")
    results['hash_signatures'] = generate_hash_signatures(apk_path)
    
    # 5. Информация о пакете
    print("\n📦 Извлекаем информацию о пакете...")
    results['package_info'] = extract_package_info(apk_path)
    
    return results

def get_apk_basic_info(apk_path):
    """Получает основную информацию об APK"""
    info = {}
    
    try:
        # Размер файла
        info['file_size'] = os.path.getsize(apk_path)
        info['file_size_mb'] = round(info['file_size'] / (1024 * 1024), 2)
        
        # MD5, SHA1, SHA256 всего APK
        with open(apk_path, 'rb') as f:
            data = f.read()
            info['md5'] = hashlib.md5(data).hexdigest()
            info['sha1'] = hashlib.sha1(data).hexdigest()
            info['sha256'] = hashlib.sha256(data).hexdigest()
        
        print(f"  ✅ Размер: {info['file_size_mb']} MB")
        print(f"  ✅ MD5: {info['md5']}")
        print(f"  ✅ SHA256: {info['sha256'][:32]}...")
        
    except Exception as e:
        print(f"  ❌ Ошибка получения основной информации: {e}")
    
    return info

def extract_certificate_signatures(apk_path):
    """Извлекает подписи из сертификатов APK"""
    signatures = []
    
    try:
        # Используем keytool для анализа подписи
        with tempfile.TemporaryDirectory() as temp_dir:
            # Извлекаем META-INF
            with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                meta_files = [f for f in apk_zip.namelist() if f.startswith('META-INF/')]
                
                for meta_file in meta_files:
                    if meta_file.endswith(('.RSA', '.DSA', '.EC')):
                        cert_path = os.path.join(temp_dir, os.path.basename(meta_file))
                        with open(cert_path, 'wb') as cert_file:
                            cert_file.write(apk_zip.read(meta_file))
                        
                        # Анализируем сертификат
                        cert_info = analyze_certificate(cert_path)
                        if cert_info:
                            signatures.append(cert_info)
        
        print(f"  ✅ Найдено сертификатов: {len(signatures)}")
        
    except Exception as e:
        print(f"  ❌ Ошибка извлечения сертификатов: {e}")
    
    return signatures

def analyze_certificate(cert_path):
    """Анализирует сертификат и извлекает подписи"""
    try:
        # Используем openssl для анализа
        result = subprocess.run([
            'openssl', 'pkcs7', '-inform', 'DER', '-in', cert_path, 
            '-print_certs', '-text', '-noout'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            cert_text = result.stdout
            
            # Извлекаем отпечатки
            fingerprints = extract_fingerprints_from_cert(cert_text)
            
            # Дополнительно пробуем извлечь подпись другим способом
            sig_result = subprocess.run([
                'openssl', 'pkcs7', '-inform', 'DER', '-in', cert_path, '-print_certs'
            ], capture_output=True, text=True)
            
            if sig_result.returncode == 0:
                # Извлекаем PEM сертификат и вычисляем его хеши
                pem_cert = sig_result.stdout
                additional_sigs = process_pem_certificate(pem_cert)
                fingerprints.update(additional_sigs)
            
            return fingerprints
            
    except Exception as e:
        print(f"    ❌ Ошибка анализа сертификата: {e}")
    
    return None

def extract_fingerprints_from_cert(cert_text):
    """Извлекает отпечатки из текста сертификата"""
    fingerprints = {}
    
    # Ищем различные типы отпечатков
    patterns = {
        'sha1': r'SHA1[:\s]+([a-fA-F0-9:]{59})',
        'sha256': r'SHA256[:\s]+([a-fA-F0-9:]{95})',
        'md5': r'MD5[:\s]+([a-fA-F0-9:]{47})'
    }
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, cert_text, re.IGNORECASE)
        if matches:
            # Убираем двоеточия и конвертируем в разные форматы
            clean_hash = matches[0].replace(':', '')
            fingerprints[f'{name}_fingerprint'] = clean_hash
            fingerprints[f'{name}_base64'] = base64.b64encode(bytes.fromhex(clean_hash)).decode()
    
    return fingerprints

def process_pem_certificate(pem_cert):
    """Обрабатывает PEM сертификат и извлекает дополнительные подписи"""
    signatures = {}
    
    try:
        # Вычисляем хеши PEM сертификата
        cert_bytes = pem_cert.encode('utf-8')
        signatures['pem_sha1'] = hashlib.sha1(cert_bytes).hexdigest()
        signatures['pem_sha256'] = hashlib.sha256(cert_bytes).hexdigest()
        signatures['pem_md5'] = hashlib.md5(cert_bytes).hexdigest()
        
        # Base64 варианты
        signatures['pem_sha1_base64'] = base64.b64encode(hashlib.sha1(cert_bytes).digest()).decode()
        signatures['pem_sha256_base64'] = base64.b64encode(hashlib.sha256(cert_bytes).digest()).decode()
        
    except Exception as e:
        print(f"    ❌ Ошибка обработки PEM: {e}")
    
    return signatures

def extract_embedded_signatures(apk_path):
    """Ищет встроенные подписи в коде APK"""
    signatures = []
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            # Ищем в разных типах файлов
            for file_info in apk_zip.infolist():
                if file_info.filename.endswith(('.dex', '.xml', '.txt', '.json', '.properties')):
                    try:
                        content = apk_zip.read(file_info.filename)
                        found_sigs = search_signatures_in_content(content, file_info.filename)
                        signatures.extend(found_sigs)
                    except:
                        continue
        
        # Удаляем дубликаты
        unique_signatures = []
        seen = set()
        for sig in signatures:
            sig_key = f"{sig['type']}:{sig['value']}"
            if sig_key not in seen:
                seen.add(sig_key)
                unique_signatures.append(sig)
        
        print(f"  ✅ Найдено встроенных подписей: {len(unique_signatures)}")
        
    except Exception as e:
        print(f"  ❌ Ошибка поиска встроенных подписей: {e}")
    
    return unique_signatures

def search_signatures_in_content(content, filename):
    """Ищет подписи в содержимом файла"""
    signatures = []
    
    try:
        # Пробуем как текст
        try:
            text_content = content.decode('utf-8', errors='ignore')
        except:
            text_content = content.decode('latin-1', errors='ignore')
        
        # Паттерны для поиска подписей
        patterns = {
            'base64_signature': r'[A-Za-z0-9+/]{40,}={0,2}',
            'hex_signature': r'[a-fA-F0-9]{32,}',
            'sha_pattern': r'[a-fA-F0-9]{40}',
            'sha256_pattern': r'[a-fA-F0-9]{64}',
            'signature_method': r'(checkSignature|verifySignature|validateSignature|getSignature)',
            'package_signature': r'(me\.bmax\.apatch|APatch|signature)',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 16:  # Минимальная длина для подписи
                    signatures.append({
                        'type': pattern_name,
                        'value': match,
                        'source_file': filename,
                        'length': len(match)
                    })
        
        # Также ищем в бинарном содержимом
        binary_sigs = search_binary_signatures(content, filename)
        signatures.extend(binary_sigs)
        
    except Exception as e:
        pass
    
    return signatures

def search_binary_signatures(content, filename):
    """Ищет подписи в бинарном содержимом"""
    signatures = []
    
    try:
        # Ищем известные паттерны APatch
        known_patterns = [
            b'1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=',
            b'sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4=',
            b'me.bmax.apatch',
            b'APApplication',
            b'verifyAppSignature',
            b'checkSignature',
            b'verifySignature'
        ]
        
        for pattern in known_patterns:
            if pattern in content:
                signatures.append({
                    'type': 'known_pattern',
                    'value': pattern.decode('utf-8', errors='ignore'),
                    'source_file': filename,
                    'binary': True
                })
    
    except Exception as e:
        pass
    
    return signatures

def generate_hash_signatures(apk_path):
    """Генерирует различные хеши APK"""
    hashes = {}
    
    try:
        with open(apk_path, 'rb') as f:
            content = f.read()
        
        # Различные хеши всего файла
        hashes['full_md5'] = hashlib.md5(content).hexdigest()
        hashes['full_sha1'] = hashlib.sha1(content).hexdigest()
        hashes['full_sha256'] = hashlib.sha256(content).hexdigest()
        
        # Base64 версии
        hashes['full_md5_base64'] = base64.b64encode(hashlib.md5(content).digest()).decode()
        hashes['full_sha1_base64'] = base64.b64encode(hashlib.sha1(content).digest()).decode()
        hashes['full_sha256_base64'] = base64.b64encode(hashlib.sha256(content).digest()).decode()
        
        # Хеши без подписи (удаляем META-INF)
        unsigned_content = remove_signature_from_apk(apk_path)
        if unsigned_content:
            hashes['unsigned_md5'] = hashlib.md5(unsigned_content).hexdigest()
            hashes['unsigned_sha1'] = hashlib.sha1(unsigned_content).hexdigest()
            hashes['unsigned_sha256'] = hashlib.sha256(unsigned_content).hexdigest()
            hashes['unsigned_sha1_base64'] = base64.b64encode(hashlib.sha1(unsigned_content).digest()).decode()
        
        print(f"  ✅ Сгенерировано хешей: {len(hashes)}")
        
    except Exception as e:
        print(f"  ❌ Ошибка генерации хешей: {e}")
    
    return hashes

def remove_signature_from_apk(apk_path):
    """Удаляет подпись из APK и возвращает содержимое"""
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            with zipfile.ZipFile(apk_path, 'r') as source_zip:
                with zipfile.ZipFile(temp_file.name, 'w') as target_zip:
                    for item in source_zip.infolist():
                        if not item.filename.startswith('META-INF/'):
                            target_zip.writestr(item, source_zip.read(item.filename))
            
            temp_file.seek(0)
            return temp_file.read()
    
    except Exception as e:
        print(f"    ❌ Ошибка удаления подписи: {e}")
        return None

def extract_package_info(apk_path):
    """Извлекает информацию о пакете из APK"""
    info = {}
    
    try:
        # Используем aapt для получения информации о пакете
        result = subprocess.run([
            'aapt', 'dump', 'badging', apk_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            
            # Извлекаем основную информацию
            package_match = re.search(r"package: name='([^']+)'", output)
            if package_match:
                info['package_name'] = package_match.group(1)
            
            version_match = re.search(r"versionName='([^']+)'", output)
            if version_match:
                info['version_name'] = version_match.group(1)
                
            version_code_match = re.search(r"versionCode='([^']+)'", output)
            if version_code_match:
                info['version_code'] = version_code_match.group(1)
                
            # Извлекаем информацию о приложении
            app_match = re.search(r"application: label='([^']+)'", output)
            if app_match:
                info['app_label'] = app_match.group(1)
        
        # Дополнительная информация из манифеста
        manifest_info = extract_manifest_info(apk_path)
        info.update(manifest_info)
        
        print(f"  ✅ Пакет: {info.get('package_name', 'неизвестно')}")
        print(f"  ✅ Версия: {info.get('version_name', 'неизвестно')}")
        
    except Exception as e:
        print(f"  ❌ Ошибка извлечения информации о пакете: {e}")
    
    return info

def extract_manifest_info(apk_path):
    """Извлекает дополнительную информацию из AndroidManifest.xml"""
    info = {}
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            if 'AndroidManifest.xml' in apk_zip.namelist():
                manifest_content = apk_zip.read('AndroidManifest.xml')
                
                # Ищем интересные строки (даже в бинарном виде)
                if b'me.bmax.apatch' in manifest_content:
                    info['contains_apatch_package'] = True
                
                if b'APApplication' in manifest_content:
                    info['contains_app_class'] = True
                    
                # Можно добавить больше проверок
                
    except Exception as e:
        pass
    
    return info

def save_results(results, output_file):
    """Сохраняет результаты в файл"""
    try:
        import json
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Результаты сохранены в: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Ошибка сохранения: {e}")

def print_summary(results):
    """Выводит краткую сводку результатов"""
    print("\n" + "=" * 50)
    print("📋 КРАТКАЯ СВОДКА ИЗВЛЕЧЕННЫХ ПОДПИСЕЙ")
    print("=" * 50)
    
    # Информация об APK
    apk_info = results.get('apk_info', {})
    print(f"\n📱 APK информация:")
    print(f"  • Размер: {apk_info.get('file_size_mb', 'неизвестно')} MB")
    print(f"  • SHA256: {apk_info.get('sha256', 'неизвестно')[:32]}...")
    
    # Информация о пакете
    package_info = results.get('package_info', {})
    print(f"\n📦 Пакет информация:")
    print(f"  • Имя пакета: {package_info.get('package_name', 'неизвестно')}")
    print(f"  • Версия: {package_info.get('version_name', 'неизвестно')}")
    
    # Подписи сертификатов
    cert_sigs = results.get('cert_signatures', [])
    print(f"\n🔐 Подписи сертификатов: {len(cert_sigs)}")
    for i, cert in enumerate(cert_sigs):
        print(f"  • Сертификат {i+1}:")
        for key, value in cert.items():
            if 'base64' in key:
                print(f"    - {key}: {value}")
    
    # Встроенные подписи
    embedded_sigs = results.get('embedded_signatures', [])
    print(f"\n🔍 Встроенные подписи: {len(embedded_sigs)}")
    important_sigs = [sig for sig in embedded_sigs if len(sig.get('value', '')) > 30]
    for sig in important_sigs[:10]:  # Показываем только первые 10
        print(f"  • {sig.get('type', 'unknown')}: {sig.get('value', '')[:50]}...")
    
    # Хеши
    hash_sigs = results.get('hash_signatures', {})
    print(f"\n🔧 Сгенерированные хеши:")
    for key, value in hash_sigs.items():
        if 'base64' in key:
            print(f"  • {key}: {value}")

def print_secrets_format(results):
    """Выводит подписи в формате для GitHub Secrets"""
    print("\n" + "=" * 60)
    print("🔑 ПОДПИСИ ДЛЯ GITHUB SECRETS")
    print("=" * 60)
    
    print("\n# Добавьте эти секреты в ваш GitHub репозиторий:")
    print("# Settings → Secrets and variables → Actions → New repository secret\n")
    
    # Пробуем найти наиболее подходящие подписи
    cert_sigs = results.get('cert_signatures', [])
    hash_sigs = results.get('hash_signatures', {})
    embedded_sigs = results.get('embedded_signatures', [])
    
    # APATCH_REAL_SIGNATURE - пробуем разные варианты
    candidates = []
    
    # Из сертификатов
    for cert in cert_sigs:
        for key, value in cert.items():
            if 'sha1_base64' in key:
                candidates.append(('cert_sha1_base64', value))
            elif 'sha256_base64' in key:
                candidates.append(('cert_sha256_base64', value))
    
    # Из хешей
    if 'unsigned_sha1_base64' in hash_sigs:
        candidates.append(('unsigned_sha1_base64', hash_sigs['unsigned_sha1_base64']))
    if 'full_sha1_base64' in hash_sigs:
        candidates.append(('full_sha1_base64', hash_sigs['full_sha1_base64']))
    
    # Из встроенных подписей
    for sig in embedded_sigs:
        if sig.get('type') == 'known_pattern' and '=' in sig.get('value', ''):
            candidates.append(('embedded', sig.get('value')))
    
    print("# Основные подписи (попробуйте по очереди):")
    print("APATCH_REAL_SIGNATURE=")
    for i, (source, value) in enumerate(candidates[:5]):
        print(f"# Вариант {i+1} ({source}): {value}")
    
    print(f"\nAPATCH_CODE_SIGNATURE=")
    for i, (source, value) in enumerate(candidates[:5]):
        print(f"# Вариант {i+1} ({source}): {value}")
    
    # Информация о пакете
    package_info = results.get('package_info', {})
    print(f"\nAPATCH_PACKAGE_NAME={package_info.get('package_name', 'me.bmax.apatch')}")
    print(f"APATCH_APP_CLASS=APApplication")
    print(f"APATCH_SIGNATURE_METHOD=verifyAppSignature")

def main():
    print_banner()
    
    if len(sys.argv) != 2:
        print("❌ Использование: python3 extract_signatures_from_apk.py <путь_к_apk>")
        print("\nПример:")
        print("  python3 extract_signatures_from_apk.py APatch-11107-release.apk")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    
    if not os.path.exists(apk_path):
        print(f"❌ APK файл не найден: {apk_path}")
        sys.exit(1)
    
    # Проверяем наличие необходимых инструментов
    required_tools = ['aapt', 'openssl']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True)
        except FileNotFoundError:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"⚠️  Отсутствуют инструменты: {', '.join(missing_tools)}")
        print("Установите их:")
        print("  sudo apt-get install aapt openssl")
        print("\nПродолжаем без этих инструментов...\n")
    
    # Извлекаем подписи
    results = extract_apk_signatures(apk_path)
    
    if results:
        # Выводим сводку
        print_summary(results)
        
        # Выводим в формате для GitHub Secrets
        print_secrets_format(results)
        
        # Сохраняем в файл
        output_file = f"signatures_{Path(apk_path).stem}.json"
        save_results(results, output_file)
        
        print(f"\n🎉 Анализ завершен! Используйте найденные подписи в ваших секретах.")
    else:
        print("\n❌ Не удалось извлечь подписи из APK")
        sys.exit(1)

if __name__ == "__main__":
    main()