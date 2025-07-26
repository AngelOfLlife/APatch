# Извлечение подписи из готового APK APatch

## 📥 Скачивание готового APK

Скачайте последний релиз APatch:
- **URL**: https://github.com/bmax121/APatch/releases
- **Файл**: `APatch-v[version]-release.apk`

## 🔧 Способ 1: Автоматическое извлечение (GitHub Actions)

Создайте workflow для автоматического скачивания и извлечения подписи:

```yaml
name: Extract APatch Signature from Release

on:
  workflow_dispatch:

jobs:
  extract-signature:
    runs-on: ubuntu-latest
    
    steps:
    - name: Download latest APatch release
      run: |
        # Получить URL последнего релиза
        LATEST_URL=$(curl -s https://api.github.com/repos/bmax121/APatch/releases/latest | grep "browser_download_url.*apk" | cut -d '"' -f 4)
        echo "Latest APK URL: $LATEST_URL"
        
        # Скачать APK
        wget -O apatch-release.apk "$LATEST_URL"
        ls -la apatch-release.apk
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Create signature extraction script
      run: |
        cat > extract_signature.py << 'EOF'
        #!/usr/bin/env python3
        import zipfile
        import hashlib
        import base64
        import sys
        import os
        
        def extract_apatch_signature(apk_path):
            if not os.path.exists(apk_path):
                print(f"File {apk_path} not found")
                return None
                
            try:
                with zipfile.ZipFile(apk_path, 'r') as apk:
                    cert_files = []
                    for file_name in apk.namelist():
                        if file_name.startswith('META-INF/') and (file_name.endswith('.RSA') or file_name.endswith('.DSA')):
                            cert_files.append(file_name)
                    
                    if not cert_files:
                        print("Certificate files not found in APK")
                        return None
                        
                    print(f"Found certificate files: {cert_files}")
                    cert_file = cert_files[0]
                    cert_data = apk.read(cert_file)
                    
                    print(f"Certificate size: {len(cert_data)} bytes")
                    
                    # APatch uses SHA256 hash of certificate data
                    sha256_hash = hashlib.sha256(cert_data).digest()
                    signature_base64 = base64.b64encode(sha256_hash).decode('utf-8')
                    
                    return signature_base64
                    
            except Exception as e:
                print(f"Error processing APK: {e}")
                return None
        
        if __name__ == "__main__":
            signature = extract_apatch_signature("apatch-release.apk")
            if signature:
                print(f"SIGNATURE: {signature}")
            else:
                sys.exit(1)
        EOF
        
    - name: Extract signature from APK
      id: extract
      run: |
        SIGNATURE=$(python3 extract_signature.py)
        echo "Extracted signature from official APK:"
        echo "$SIGNATURE"
        
        # Сохранить только подпись
        CLEAN_SIGNATURE=$(echo "$SIGNATURE" | grep "SIGNATURE:" | cut -d' ' -f2)
        echo "signature=$CLEAN_SIGNATURE" >> $GITHUB_OUTPUT
        
    - name: Create signature information
      run: |
        cat > apatch_official_signature.txt << EOF
        APatch Official Signature Information
        ====================================
        
        Extracted from: Official APatch Release
        Source: https://github.com/bmax121/APatch/releases
        Date: $(date)
        
        Original APatch Signature:
        ${{ steps.extract.outputs.signature }}
        
        Usage in your APatch builds:
        ===========================
        
        Replace in app/src/main/java/me/bmax/apatch/APatchApp.kt:
        
        OLD:
        verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")
        
        NEW:
        verifyAppSignature("${{ steps.extract.outputs.signature }}")
        
        Note: This signature should match the original one if extracted correctly.
        If they don't match, there might be a version difference or extraction issue.
        EOF
        
    - name: Upload signature info
      uses: actions/upload-artifact@v4
      with:
        name: APatch-Official-Signature
        path: apatch_official_signature.txt
        
    - name: Compare with known signature
      run: |
        KNOWN_SIGNATURE="1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
        EXTRACTED_SIGNATURE="${{ steps.extract.outputs.signature }}"
        
        echo "Known signature:     $KNOWN_SIGNATURE"
        echo "Extracted signature: $EXTRACTED_SIGNATURE"
        
        if [ "$KNOWN_SIGNATURE" = "$EXTRACTED_SIGNATURE" ]; then
            echo "✅ Signatures match! Extraction is correct."
        else
            echo "⚠️  Signatures don't match. This might be:"
            echo "   - Different APatch version"
            echo "   - Different signing key"
            echo "   - Extraction method difference"
        fi
```

## 🛠️ Способ 2: Локальное извлечение

1. **Скачайте APK вручную**:
   ```bash
   # Или скачайте через браузер с https://github.com/bmax121/APatch/releases
   wget https://github.com/bmax121/APatch/releases/download/[version]/APatch-[version]-release.apk
   ```

2. **Извлеките подпись**:
   ```bash
   python3 extract_apatch_signature.py APatch-[version]-release.apk
   ```

3. **Результат**:
   ```
   APatch signature: 1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=
   ```

## 🔍 Проверка вашей подписи

Если вы хотите заменить оригинальную подпись на свою:

```bash
# 1. Извлечь подпись из оригинального APK
python3 extract_apatch_signature.py APatch-original.apk

# 2. Извлечь подпись из вашего APK
python3 extract_apatch_signature.py your-custom-apk.apk

# 3. Сравнить результаты
```

## 📋 Быстрые команды

### Скачать последний релиз:
```bash
# Получить URL последнего релиза
LATEST_URL=$(curl -s https://api.github.com/repos/bmax121/APatch/releases/latest | grep "browser_download_url.*apk" | cut -d '"' -f 4)

# Скачать
wget -O apatch-latest.apk "$LATEST_URL"
```

### Извлечь подпись одной командой:
```bash
# Скачать и извлечь
curl -s https://api.github.com/repos/bmax121/APatch/releases/latest | grep "browser_download_url.*apk" | cut -d '"' -f 4 | xargs wget -O apatch.apk && python3 extract_apatch_signature.py apatch.apk
```

## 🎯 Использование результата

После извлечения подписи из оригинального APK:

1. **Если подписи совпадают** с известной (`1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=`):
   - Извлечение корректно
   - Используйте эту подпись в своих сборках

2. **Если подписи отличаются**:
   - Возможно, изменился ключ подписи в новой версии
   - Используйте извлеченную подпись как правильную

3. **Для создания собственной версии**:
   - Замените подпись в коде на подпись ваших ключей
   - Следуйте инструкциям из `generate_correct_signature.md`

## ⚡ GitHub Secret для автоматизации

После извлечения добавьте в GitHub Secrets:

```bash
gh secret set APATCH_OFFICIAL_SIGNATURE --body "ИЗВЛЕЧЕННАЯ_ПОДПИСЬ"
```

Теперь вы можете использовать `${{ secrets.APATCH_OFFICIAL_SIGNATURE }}` в ваших workflows.