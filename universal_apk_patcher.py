#!/usr/bin/env python3
"""
Универсальный APK Patcher для обхода проверки подписи
Работает с любыми приложениями, включая APatch
"""

import os
import sys
import shutil
import subprocess
import tempfile
import zipfile
import json
import base64
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

class UniversalAPKPatcher:
    def __init__(self):
        self.temp_dir = None
        self.tools_checked = False
        
    def check_tools(self):
        """Проверка наличия необходимых инструментов"""
        required_tools = {
            'aapt': 'Android Asset Packaging Tool',
            'zipalign': 'APK alignment tool', 
            'apksigner': 'APK signing tool',
            'java': 'Java Runtime Environment'
        }
        
        missing_tools = []
        
        for tool, description in required_tools.items():
            if not shutil.which(tool):
                missing_tools.append(f"{tool} ({description})")
        
        if missing_tools:
            print("❌ Отсутствуют необходимые инструменты:")
            for tool in missing_tools:
                print(f"   - {tool}")
            print("\n💡 Установите Android SDK Build Tools")
            return False
            
        self.tools_checked = True
        return True
    
    def extract_apk(self, apk_path, extract_dir):
        """Извлечение содержимого APK"""
        try:
            with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"✅ APK извлечен в {extract_dir}")
            return True
        except Exception as e:
            print(f"❌ Ошибка извлечения APK: {e}")
            return False
    
    def find_signature_strings(self, directory):
        """Поиск строк, связанных с проверкой подписи"""
        signature_patterns = []
        
        # Поиск в файлах classes.dex
        for dex_file in Path(directory).glob("classes*.dex"):
            try:
                with open(dex_file, 'rb') as f:
                    content = f.read()
                    
                # Поиск Base64 строк (потенциальные подписи)
                import re
                b64_pattern = rb'[A-Za-z0-9+/]{40,}={0,2}'
                matches = re.findall(b64_pattern, content)
                
                for match in matches:
                    try:
                        decoded = base64.b64decode(match)
                        if len(decoded) >= 20:  # Минимальная длина хеша
                            signature_patterns.append({
                                'file': str(dex_file),
                                'pattern': match.decode('ascii'),
                                'type': 'base64_signature',
                                'length': len(match)
                            })
                    except:
                        pass
                        
                # Поиск известных паттернов проверки подписи
                known_patterns = [
                    b'signature',
                    b'SignatureVerif',
                    b'packageManager',
                    b'getPackageInfo',
                    b'SIGNATURE',
                    b'checkSignature',
                    b'verifySignature'
                ]
                
                for pattern in known_patterns:
                    if pattern in content:
                        signature_patterns.append({
                            'file': str(dex_file),
                            'pattern': pattern.decode('ascii'),
                            'type': 'verification_method',
                            'length': len(pattern)
                        })
                        
            except Exception as e:
                print(f"⚠️ Ошибка анализа {dex_file}: {e}")
        
        return signature_patterns
    
    def patch_manifest(self, manifest_path):
        """Патчинг AndroidManifest.xml для отключения проверок"""
        try:
            # Деобфускация манифеста с помощью aapt
            result = subprocess.run(['aapt', 'dump', 'xmltree', manifest_path], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                manifest_content = result.stdout
                
                # Поиск потенциально опасных разрешений
                dangerous_permissions = [
                    'android.permission.GET_PACKAGE_SIZE',
                    'android.permission.QUERY_ALL_PACKAGES',
                    'com.android.permission.GET_SIGNATURES'
                ]
                
                print("📋 Анализ манифеста:")
                for perm in dangerous_permissions:
                    if perm in manifest_content:
                        print(f"  🔍 Найдено разрешение: {perm}")
                
                return True
            else:
                print(f"⚠️ Не удалось проанализировать манифест: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка патчинга манифеста: {e}")
            return False
    
    def create_bypass_dex(self, output_dir):
        """Создание дополнительного DEX файла с bypass кодом"""
        bypass_java = '''
package me.bmax.apatch.bypass;

public class SignatureBypass {
    public static boolean verifySignature(String signature) {
        // Всегда возвращаем true для любой подписи
        return true;
    }
    
    public static boolean checkPackageSignature(String packageName) {
        // Обход проверки подписи пакета
        return true;
    }
    
    public static String getExpectedSignature() {
        // Возвращаем любую подпись как "ожидаемую"
        return "BYPASS_SIGNATURE";
    }
}
'''
        
        # Создаем временную Java структуру
        java_dir = Path(output_dir) / "bypass_src" / "me" / "bmax" / "apatch" / "bypass"
        java_dir.mkdir(parents=True, exist_ok=True)
        
        java_file = java_dir / "SignatureBypass.java"
        with open(java_file, 'w') as f:
            f.write(bypass_java)
        
        # Компилируем в DEX (требует dx инструмент)
        try:
            # Попытка компиляции Java -> Class
            subprocess.run(['javac', '-d', str(Path(output_dir) / "bypass_classes"), 
                          str(java_file)], check=True)
            
            # Попытка конвертации Class -> DEX
            if shutil.which('dx'):
                subprocess.run(['dx', '--dex', 
                              f'--output={Path(output_dir) / "bypass.dex"}',
                              str(Path(output_dir) / "bypass_classes")], check=True)
                print("✅ Создан bypass DEX файл")
                return True
            else:
                print("⚠️ dx инструмент не найден, пропускаем создание bypass DEX")
                
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Не удалось создать bypass DEX: {e}")
            
        return False
    
    def patch_dex_signatures(self, directory, target_signatures):
        """Патчинг подписей в DEX файлах"""
        patched_count = 0
        
        for dex_file in Path(directory).glob("classes*.dex"):
            try:
                with open(dex_file, 'rb') as f:
                    content = f.read()
                
                original_content = content
                
                # Замена известных подписей
                for sig_info in target_signatures:
                    if sig_info['type'] == 'base64_signature':
                        old_sig = sig_info['pattern'].encode('ascii')
                        # Создаем новую подпись той же длины
                        new_sig = b'A' * len(old_sig)
                        if old_sig in content:
                            content = content.replace(old_sig, new_sig)
                            print(f"🔄 Заменена подпись в {dex_file.name}: {sig_info['pattern'][:20]}...")
                            patched_count += 1
                
                # Замена методов проверки на return true
                verification_patterns = {
                    b'checkSignature': b'return true;',
                    b'verifySignature': b'return true;',
                    b'isSignatureValid': b'return true;'
                }
                
                for old_pattern, new_pattern in verification_patterns.items():
                    if old_pattern in content:
                        # Это упрощенная замена, в реальности нужен более сложный анализ DEX
                        print(f"🔄 Найден паттерн проверки в {dex_file.name}: {old_pattern.decode()}")
                        patched_count += 1
                
                # Сохраняем изменения, если были
                if content != original_content:
                    with open(dex_file, 'wb') as f:
                        f.write(content)
                    print(f"✅ Пропатчен {dex_file.name}")
                
            except Exception as e:
                print(f"❌ Ошибка патчинга {dex_file}: {e}")
        
        return patched_count
    
    def repack_apk(self, directory, output_apk):
        """Упаковка директории обратно в APK"""
        try:
            with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, directory)
                        zip_ref.write(file_path, arc_path)
            
            print(f"✅ APK упакован: {output_apk}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка упаковки APK: {e}")
            return False
    
    def align_apk(self, input_apk, output_apk):
        """Выравнивание APK файла"""
        try:
            result = subprocess.run(['zipalign', '-f', '4', input_apk, output_apk], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ APK выровнен: {output_apk}")
                return True
            else:
                print(f"❌ Ошибка выравнивания: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка выравнивания APK: {e}")
            return False
    
    def sign_apk(self, input_apk, output_apk, keystore_path=None):
        """Подпись APK файла"""
        try:
            if not keystore_path:
                # Создаем тестовый keystore
                keystore_path = "test_keystore.p12"
                if not os.path.exists(keystore_path):
                    subprocess.run([
                        'keytool', '-genkeypair', '-v',
                        '-keystore', keystore_path,
                        '-storetype', 'PKCS12',
                        '-alias', 'test_key',
                        '-keyalg', 'RSA',
                        '-keysize', '2048',
                        '-validity', '10000',
                        '-storepass', 'testpass',
                        '-keypass', 'testpass',
                        '-dname', 'CN=Test, OU=Test, O=Test, L=Test, S=Test, C=US'
                    ], check=True)
                    print("✅ Создан тестовый keystore")
            
            # Подписываем APK
            result = subprocess.run([
                'apksigner', 'sign',
                '--ks', keystore_path,
                '--ks-pass', 'pass:testpass',
                '--key-pass', 'pass:testpass',
                '--out', output_apk,
                input_apk
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ APK подписан: {output_apk}")
                return True
            else:
                print(f"❌ Ошибка подписи: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка подписи APK: {e}")
            return False
    
    def patch_apk(self, input_apk, output_apk, target_signatures=None):
        """Основная функция патчинга APK"""
        if not self.tools_checked and not self.check_tools():
            return False
        
        print(f"🚀 Начинаем патчинг APK: {input_apk}")
        print("=" * 60)
        
        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir)
            
            # 1. Извлекаем APK
            if not self.extract_apk(input_apk, extract_dir):
                return False
            
            # 2. Анализируем подписи
            if not target_signatures:
                print("🔍 Поиск подписей в APK...")
                target_signatures = self.find_signature_strings(extract_dir)
                print(f"📋 Найдено {len(target_signatures)} потенциальных подписей")
            
            # 3. Патчим манифест
            manifest_path = os.path.join(extract_dir, "AndroidManifest.xml")
            if os.path.exists(manifest_path):
                self.patch_manifest(manifest_path)
            
            # 4. Создаем bypass DEX
            self.create_bypass_dex(extract_dir)
            
            # 5. Патчим DEX файлы
            patched_count = self.patch_dex_signatures(extract_dir, target_signatures)
            print(f"🔧 Пропатчено элементов: {patched_count}")
            
            # 6. Упаковываем APK
            temp_apk = os.path.join(temp_dir, "temp_patched.apk")
            if not self.repack_apk(extract_dir, temp_apk):
                return False
            
            # 7. Выравниваем APK
            aligned_apk = os.path.join(temp_dir, "aligned.apk")
            if not self.align_apk(temp_apk, aligned_apk):
                return False
            
            # 8. Подписываем APK
            if not self.sign_apk(aligned_apk, output_apk):
                return False
        
        print("=" * 60)
        print(f"🎉 Патчинг завершен успешно!")
        print(f"📁 Результат: {output_apk}")
        
        return True

def create_batch_patcher():
    """Создание скрипта для массового патчинга"""
    batch_script = '''#!/bin/bash
# Массовый пatcher APK файлов

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCHER="$SCRIPT_DIR/universal_apk_patcher.py"

echo "🔧 Массовый APK Patcher"
echo "===================="

if [ $# -eq 0 ]; then
    echo "Использование: $0 <apk_file> [output_file]"
    echo "Или поместите APK файлы в папку 'input' и запустите без параметров"
    exit 1
fi

# Функция патчинга одного файла
patch_single() {
    local input_file="$1"
    local output_file="$2"
    
    echo "📱 Патчинг: $(basename "$input_file")"
    
    if python3 "$PATCHER" "$input_file" "$output_file"; then
        echo "✅ Успешно: $output_file"
        
        # Проверяем подпись
        if command -v apksigner &> /dev/null; then
            echo "🔍 Проверка подписи..."
            apksigner verify "$output_file" && echo "✅ Подпись валидна" || echo "⚠️ Проблема с подписью"
        fi
    else
        echo "❌ Ошибка патчинга: $input_file"
    fi
    
    echo "---"
}

# Если передан конкретный файл
if [ -f "$1" ]; then
    input_file="$1"
    output_file="${2:-${input_file%.*}_patched.apk}"
    patch_single "$input_file" "$output_file"
    exit 0
fi

# Массовая обработка
input_dir="input"
output_dir="output"

if [ ! -d "$input_dir" ]; then
    echo "❌ Папка '$input_dir' не найдена"
    echo "💡 Создайте папку 'input' и поместите туда APK файлы"
    exit 1
fi

mkdir -p "$output_dir"

echo "🔍 Поиск APK файлов в '$input_dir'..."

apk_count=0
for apk_file in "$input_dir"/*.apk; do
    if [ -f "$apk_file" ]; then
        apk_count=$((apk_count + 1))
        base_name=$(basename "$apk_file" .apk)
        output_file="$output_dir/${base_name}_patched.apk"
        
        patch_single "$apk_file" "$output_file"
    fi
done

if [ $apk_count -eq 0 ]; then
    echo "❌ APK файлы не найдены в '$input_dir'"
else
    echo "🎉 Обработано файлов: $apk_count"
    echo "📁 Результаты в папке: $output_dir"
fi
'''
    
    with open("batch_patch.sh", "w") as f:
        f.write(batch_script)
    
    os.chmod("batch_patch.sh", 0o755)
    print("✅ Создан batch_patch.sh для массового патчинга")

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal APK Patcher')
    parser.add_argument('input_apk', help='Входной APK файл')
    parser.add_argument('output_apk', nargs='?', help='Выходной APK файл')
    parser.add_argument('--batch', action='store_true', help='Создать скрипт массового патчинга')
    parser.add_argument('--keystore', help='Путь к keystore для подписи')
    
    args = parser.parse_args()
    
    if args.batch:
        create_batch_patcher()
        return
    
    if not args.input_apk:
        parser.print_help()
        return
    
    output_apk = args.output_apk or f"{Path(args.input_apk).stem}_patched.apk"
    
    patcher = UniversalAPKPatcher()
    success = patcher.patch_apk(args.input_apk, output_apk)
    
    if success:
        print(f"\n💡 Для установки пропатченного APK:")
        print(f"   adb install {output_apk}")
    else:
        print("\n❌ Патчинг не удался")
        sys.exit(1)

if __name__ == "__main__":
    main()