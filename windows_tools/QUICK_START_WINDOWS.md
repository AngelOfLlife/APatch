# ⚡ Быстрый старт для Windows 10

## 🎯 Цель: Получить подписи APatch за 5 минут

### 📥 1. Скачайте файлы (2 минуты)

```
1. Создайте папку: C:\APatch_Extractor\
2. Скачайте в эту папку:
   • windows_quick_extract.py
   • extract_apatch_windows.bat
3. Скачайте оригинальный APK APatch
```

### 🐍 2. Проверьте Python (30 секунд)

```cmd
# Откройте cmd и выполните:
python --version

# Если ошибка - установите Python:
# https://www.python.org/downloads/
# ОБЯЗАТЕЛЬНО отметьте "Add Python to PATH"
```

### 🖱️ 3. Извлеките подписи (1 минута)

**Простейший способ:**
```
1. Откройте папку C:\APatch_Extractor\
2. Перетащите APK файл на extract_apatch_windows.bat
3. Дождитесь результата
```

**Альтернативный способ:**
```cmd
cd C:\APatch_Extractor\
extract_apatch_windows.bat "APatch-11107-release.apk"
```

### 📋 4. Скопируйте результат (30 секунд)

Найдите в выводе:
```
APATCH_REAL_SIGNATURE=oR6DrWQ8yJaV7BKtQ9nF2xR7Plw=
APATCH_CODE_SIGNATURE=nK5bQ2r8vF3pAzM6yHgN1cXkS9wE=
```

### 🔑 5. Обновите GitHub Secrets (1 минута)

```
1. Перейдите: https://github.com/AngelOfLlife/APatch/settings/secrets/actions
2. Нажмите на APATCH_REAL_SIGNATURE → Update
3. Вставьте новое значение → Update secret
4. Повторите для APATCH_CODE_SIGNATURE
```

### 🚀 6. Запустите сборку

```
1. Перейдите: https://github.com/AngelOfLlife/APatch/actions
2. Выберите любой workflow
3. Нажмите "Run workflow"
4. Дождитесь завершения (15-30 минут)
5. Скачайте готовый APK без зависания!
```

---

## 🆘 Если что-то не работает:

### ❌ Python не найден
```cmd
# Переустановите Python с "Add to PATH"
# Или используйте полный путь:
C:\Python39\python.exe windows_quick_extract.py APatch.apk
```

### ❌ Файл не найден
```cmd
# Проверьте путь (используйте кавычки для путей с пробелами):
extract_apatch_windows.bat "C:\Downloads\APatch APK.apk"
```

### ❌ Доступ запрещен
```cmd
# Запустите cmd от имени администратора:
# Win+X → "Windows PowerShell (Администратор)"
```

---

## 💡 Результат

После использования **ТОЧНЫХ** подписей из оригинального APK:
- ✅ **Зависание ИСЧЕЗНЕТ**
- ✅ **APatch будет работать**
- ✅ **Root функции доступны**

**Время выполнения: ~5 минут**
**Требования: Python + оригинальный APK**
**Результат: Рабочий APatch без зависания** 🎉