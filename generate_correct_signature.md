# Генерация правильной подписи для APatch

## Цель
Получить правильный хеш подписи для ваших ключей и заменить его в коде APatch, чтобы проверка подписи проходила успешно.

## Шаги решения

### 1. Создание тестового APK с вашими ключами

Сначала создайте временный APK для получения подписи:

**GitHub Actions workflow для получения подписи:**

```yaml
name: Generate APatch Signature
on: 
  workflow_dispatch:

jobs:
  generate-signature:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          
      - name: Decode Signing Key
        run: |
          echo "${{ secrets.SIGNING_KEY }}" | base64 -d > keystore.p12
          
      - name: Build temporary APK
        run: ./gradlew assembleRelease
        env:
          SIGNING_KEY_PATH: keystore.p12
          ALIAS: ${{ secrets.ALIAS }}
          KEY_STORE_PASSWORD: ${{ secrets.KEY_STORE_PASSWORD }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          
      - name: Extract signature from APK
        run: |
          # Получаем сертификат из APK
          unzip -q app/build/outputs/apk/release/app-release.apk -d temp_apk/
          
          # Извлекаем подпись
          keytool -printcert -file temp_apk/META-INF/*.RSA > cert_info.txt
          
          # Получаем SHA256 отпечаток
          SHA256=$(keytool -printcert -file temp_apk/META-INF/*.RSA | grep -A1 "SHA256:" | tail -1 | tr -d ' :')
          echo "SHA256 Fingerprint: $SHA256"
          
          # Конвертируем в Base64 (как использует APatch)
          echo -n "$SHA256" | xxd -r -p | base64 > signature_base64.txt
          
          echo "Base64 signature for APatch:"
          cat signature_base64.txt
          
      - name: Upload signature info
        uses: actions/upload-artifact@v4
        with:
          name: apatch-signature
          path: |
            cert_info.txt
            signature_base64.txt
```

### 2. Альтернативный метод - локальное получение подписи

Если у вас есть готовый APK:

```bash
# Метод 1: Через keytool
keytool -printcert -jarfile app-release.apk | grep -A1 "SHA256:"

# Метод 2: Через openssl
unzip -q app-release.apk -d temp/
openssl x509 -in temp/META-INF/*.RSA -inform DER -fingerprint -sha256 -noout

# Метод 3: Получение Base64 подписи (как в APatch)
# Замените CERTIFICATE_HEX на полученный SHA256 без двоеточий
echo -n "CERTIFICATE_HEX" | xxd -r -p | base64
```

### 3. Точный метод извлечения подписи как в APatch

Создайте вспомогательный скрипт:

**extract_apatch_signature.py:**
```python
#!/usr/bin/env python3
import zipfile
import hashlib
import base64
import sys
from cryptography import x509

def extract_apatch_signature(apk_path):
    """Извлекает подпись в формате, который использует APatch"""
    
    with zipfile.ZipFile(apk_path, 'r') as apk:
        # Найти файл сертификата
        cert_files = [f for f in apk.namelist() if f.startswith('META-INF/') and f.endswith('.RSA')]
        
        if not cert_files:
            print("Файл сертификата не найден в APK")
            return None
            
        cert_file = cert_files[0]
        cert_data = apk.read(cert_file)
        
        # Парсить сертификат
        try:
            # Попробовать как PKCS#7
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.serialization import pkcs7
            
            # Загрузить PKCS#7
            p7 = pkcs7.load_der_pkcs7_certificates(cert_data)
            cert = p7[0] if p7 else None
            
            if not cert:
                # Попробовать как обычный сертификат
                cert = x509.load_der_x509_certificate(cert_data)
                
        except Exception as e:
            print(f"Ошибка при парсинге сертификата: {e}")
            return None
            
        # Получить DER-кодированный сертификат
        cert_der = cert.public_bytes(serialization.Encoding.DER)
        
        # Вычислить SHA-256
        sha256_hash = hashlib.sha256(cert_der).digest()
        
        # Конвертировать в Base64
        signature_base64 = base64.b64encode(sha256_hash).decode('utf-8')
        
        return signature_base64

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 extract_apatch_signature.py <path_to_apk>")
        sys.exit(1)
        
    apk_path = sys.argv[1]
    signature = extract_apatch_signature(apk_path)
    
    if signature:
        print(f"APatch signature: {signature}")
    else:
        print("Не удалось извлечь подпись")
```

### 4. GitHub Actions с автоматическим обновлением подписи

**Complete workflow:**

```yaml
name: Build APatch with Correct Signature
on: 
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build-with-signature:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          pip install cryptography
          
      - name: Decode Signing Key
        run: |
          echo "${{ secrets.SIGNING_KEY }}" | base64 -d > keystore.p12
          
      - name: Create signature extraction script
        run: |
          cat > extract_signature.py << 'EOF'
          import zipfile
          import hashlib
          import base64
          import sys
          from cryptography import x509
          from cryptography.hazmat.primitives import serialization
          
          def extract_signature(apk_path):
              with zipfile.ZipFile(apk_path, 'r') as apk:
                  cert_files = [f for f in apk.namelist() if f.startswith('META-INF/') and (f.endswith('.RSA') or f.endswith('.DSA'))]
                  
                  if not cert_files:
                      return None
                      
                  cert_data = apk.read(cert_files[0])
                  
                  try:
                      cert = x509.load_der_x509_certificate(cert_data)
                  except:
                      try:
                          from cryptography.hazmat.primitives.serialization import pkcs7
                          p7 = pkcs7.load_der_pkcs7_certificates(cert_data)
                          cert = p7[0] if p7 else None
                      except:
                          return None
                  
                  if not cert:
                      return None
                      
                  cert_der = cert.public_bytes(serialization.Encoding.DER)
                  sha256_hash = hashlib.sha256(cert_der).digest()
                  return base64.b64encode(sha256_hash).decode('utf-8')
          
          if __name__ == "__main__":
              signature = extract_signature(sys.argv[1])
              if signature:
                  print(signature)
          EOF
          
      - name: Build temporary APK to get signature
        run: ./gradlew assembleRelease
        env:
          SIGNING_KEY_PATH: keystore.p12
          ALIAS: ${{ secrets.ALIAS }}
          KEY_STORE_PASSWORD: ${{ secrets.KEY_STORE_PASSWORD }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          
      - name: Extract signature
        id: signature
        run: |
          NEW_SIGNATURE=$(python3 extract_signature.py app/build/outputs/apk/release/app-release.apk)
          echo "signature=$NEW_SIGNATURE" >> $GITHUB_OUTPUT
          echo "New signature: $NEW_SIGNATURE"
          
      - name: Update signature in code
        run: |
          # Заменить подпись в APatchApp.kt
          sed -i 's/verifyAppSignature("[^"]*")/verifyAppSignature("${{ steps.signature.outputs.signature }}")/' app/src/main/java/me/bmax/apatch/APatchApp.kt
          
      - name: Build final APK with correct signature
        run: ./gradlew clean assembleRelease
        env:
          SIGNING_KEY_PATH: keystore.p12
          ALIAS: ${{ secrets.ALIAS }}
          KEY_STORE_PASSWORD: ${{ secrets.KEY_STORE_PASSWORD }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
          
      - name: Upload final APK
        uses: actions/upload-artifact@v4
        with:
          name: apatch-custom-signed
          path: app/build/outputs/apk/release/*.apk
          
      - name: Show signature info
        run: |
          echo "Final signature used: ${{ steps.signature.outputs.signature }}"
          echo "Original signature was: 1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
```

### 5. Ручное обновление кода

После получения новой подписи, замените в файле `app/src/main/java/me/bmax/apatch/APatchApp.kt`:

**Было:**
```kotlin
if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
```

**Стало (замените YOUR_NEW_SIGNATURE на полученную подпись):**
```kotlin
if (!BuildConfig.DEBUG && !verifyAppSignature("YOUR_NEW_SIGNATURE")) {
```

### 6. Дополнительные GitHub Secrets

Добавьте новый секрет с правильной подписью:

```bash
# После получения новой подписи
gh secret set APATCH_CUSTOM_SIGNATURE --body "YOUR_NEW_SIGNATURE_HERE"
```

### 7. Проверка результата

После сборки с новой подписью:
- Приложение не будет зависать на логотипе
- Проверка подписи будет проходить успешно
- Безопасность приложения сохранится

## Важные замечания

✅ **Преимущества этого подхода:**
- Сохраняется оригинальная логика безопасности
- Приложение работает как оригинальное
- Проверка подписи остается активной

⚠️ **Замечания:**
- Новая подпись будет уникальной для ваших ключей
- Сохраните новую подпись для будущих сборок
- Процедуру нужно повторить при смене ключей