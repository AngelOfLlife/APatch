# Быстрое руководство: Получение правильной подписи для APatch

## 🎯 Цель
Заменить оригинальную подпись APatch на подпись ваших ключей, чтобы приложение работало без зависания.

## 🚀 Способ 1: Автоматический (GitHub Actions)

1. **Добавьте workflow файл** в `.github/workflows/build_apatch.yml`:
   - Используйте содержимое файла `build_apatch_with_signature.yml`

2. **Добавьте секреты в GitHub**:
   ```bash
   gh secret set SIGNING_KEY --body "MIIKpAIBAzCCCk4GCSqGSIb3DQEHAaCCCj8Eggo7..."
   gh secret set ALIAS --body "apatch"
   gh secret set KEY_STORE_PASSWORD --body "apatch123"
   gh secret set KEY_PASSWORD --body "apatch123"
   ```

3. **Запустите workflow**:
   - Перейдите в Actions
   - Выберите "Build APatch with Correct Signature"
   - Нажмите "Run workflow"

4. **Скачайте результат**:
   - APK будет в артефактах: `APatch-Custom-Signed.apk`
   - Информация о подписи: `Signature-Info.txt`

## 🛠️ Способ 2: Локальный

1. **Соберите APK с вашими ключами**:
   ```bash
   ./gradlew assembleRelease
   ```

2. **Извлеките подпись**:
   ```bash
   python3 extract_apatch_signature.py app-release.apk
   ```

3. **Замените подпись в коде**:
   В файле `app/src/main/java/me/bmax/apatch/APatchApp.kt` замените:
   ```kotlin
   verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")
   ```
   на:
   ```kotlin
   verifyAppSignature("ВАША_НОВАЯ_ПОДПИСЬ")
   ```

4. **Пересоберите**:
   ```bash
   ./gradlew clean assembleRelease
   ```

## 📋 Что происходит

1. **Первая сборка**: Создается APK с вашими ключами
2. **Извлечение**: Из APK извлекается SHA256 хеш сертификата в Base64
3. **Замена**: В коде заменяется оригинальная подпись на вашу
4. **Финальная сборка**: Создается окончательный APK

## ✅ Результат

- ✅ Приложение запускается без зависания
- ✅ Проверка подписи проходит успешно  
- ✅ Безопасность сохраняется
- ✅ Используются ваши ключи подписи

## 🔧 Файлы для использования

- `extract_apatch_signature.py` - Локальное извлечение подписи
- `build_apatch_with_signature.yml` - Workflow для GitHub Actions
- `generate_correct_signature.md` - Подробное руководство

## 💡 Совет

GitHub Actions workflow делает все автоматически:
1. Создает временный APK
2. Извлекает подпись
3. Обновляет код
4. Собирает финальный APK
5. Проверяет корректность

Просто запустите workflow и получите готовый APK!