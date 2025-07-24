# Исправление проблемы зависания APatch на логотипе

## Проблема
При использовании пользовательских ключей подписи приложение APatch зависает на логотипе из-за проверки подписи в коде.

## Причина
В файле `APatchApp.kt` есть проверка подписи:
```kotlin
if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
    while (true) {
        val intent = Intent(Intent.ACTION_DELETE)
        intent.data = "package:$packageName".toUri()
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS)
        startActivity(intent)
        exitProcess(0)
    }
}
```

## Решения

### Решение 1: Отключить проверку подписи (Рекомендуется)

Замените проблемный блок в `app/src/main/java/me/bmax/apatch/APatchApp.kt`:

**Исходный код:**
```kotlin
if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
    while (true) {
        val intent = Intent(Intent.ACTION_DELETE)
        intent.data = "package:$packageName".toUri()
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS)
        startActivity(intent)
        exitProcess(0)
    }
}
```

**Замените на:**
```kotlin
// Signature verification disabled for custom builds
// if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
//     while (true) {
//         val intent = Intent(Intent.ACTION_DELETE)
//         intent.data = "package:$packageName".toUri()
//         intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
//         intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS)
//         startActivity(intent)
//         exitProcess(0)
//     }
// }
```

### Решение 2: Использовать DEBUG сборку

В `app/build.gradle.kts` измените:
```kotlin
buildTypes {
    release {
        isMinifyEnabled = true
        isShrinkResources = true
        // Добавьте эту строку:
        isDebuggable = true
    }
}
```

### Решение 3: Получить правильную подпись

Если хотите использовать собственную подпись, нужно:

1. Собрать APK с вашими ключами
2. Получить SHA256 хеш подписи:

```bash
# Получить подпись из APK
keytool -printcert -jarfile app-release.apk

# Или получить Base64 представление
openssl dgst -sha256 -binary app-release.apk | openssl base64
```

3. Заменить хеш в коде на полученный

### Решение 4: Patch для автоматической сборки

Создайте patch файл `disable_signature_check.patch`:

```diff
--- a/app/src/main/java/me/bmax/apatch/APatchApp.kt
+++ b/app/src/main/java/me/bmax/apatch/APatchApp.kt
@@ -xxx,xx +xxx,xx @@ class APApplication : Application(), Thread.UncaughtExceptionHandler {
         }
 
-        if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
-            while (true) {
-                val intent = Intent(Intent.ACTION_DELETE)
-                intent.data = "package:$packageName".toUri()
-                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
-                intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS)
-                startActivity(intent)
-                exitProcess(0)
-            }
-        }
+        // Signature verification disabled for custom builds
+        // if (!BuildConfig.DEBUG && !verifyAppSignature("1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=")) {
//         //     while (true) {
//         //         val intent = Intent(Intent.ACTION_DELETE)
//         //         intent.data = "package:$packageName".toUri()
//         //         intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
//         //         intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS)
//         //         startActivity(intent)
//         //         exitProcess(0)
//         //     }
//         // }
 
         // TODO: We can't totally protect superkey from be stolen by root or LSPosed-like injection tools in user space, the only way is don't use superkey,
```

Применить patch:
```bash
git apply disable_signature_check.patch
```

## GitHub Actions workflow

Добавьте в ваш workflow автоматическое применение исправления:

```yaml
- name: Disable signature verification
  run: |
    sed -i 's/if (!BuildConfig.DEBUG && !verifyAppSignature/\/\/ if (!BuildConfig.DEBUG \&\& !verifyAppSignature/' app/src/main/java/me/bmax/apatch/APatchApp.kt
    sed -i '/while (true) {/,/}$/s/^/\/\/ /' app/src/main/java/me/bmax/apatch/APatchApp.kt

- name: Build APK
  run: ./gradlew assembleRelease
```

## Проверка исправления

После применения любого из решений:

1. Пересоберите проект
2. Установите APK
3. Приложение должно запускаться без зависания

## Важные замечания

⚠️ **Безопасность:**
- Отключение проверки подписи снижает безопасность
- Используйте только для собственных сборок
- Не распространяйте модифицированные версии

✅ **Рекомендация:**
Используйте Решение 1 (комментирование кода) как самый простой и безопасный способ.