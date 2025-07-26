# 🔑 Быстрое добавление секретов APatch

## 🎯 **Цель:**
Автоматически добавить все необходимые секреты в GitHub репозиторий с извлеченными подписями из оригинального APK.

---

## ⚡ **Два варианта скриптов:**

### 🐧 **Linux/macOS:** `quick_add_extracted_secrets.sh`
### 🖥️ **Windows:** `quick_add_extracted_secrets.bat`

---

## 📋 **Что делает скрипт:**

### ✅ **Проверяет:**
- GitHub CLI установлен и авторизован
- Доступ к указанному репозиторию

### ✅ **Запрашивает:**
- **APATCH_REAL_SIGNATURE** (извлеченная из оригинального APK)
- **APATCH_CODE_SIGNATURE** (SHA256 хеш APK)
- **Имя репозитория** (по умолчанию: AngelOfLlife/APatch)

### ✅ **Добавляет автоматически:**
- `SIGNING_KEY` - готовый keystore в base64
- `ALIAS` - apatch
- `KEY_STORE_PASSWORD` - apatch123
- `KEY_PASSWORD` - apatch123
- `APATCH_REAL_SIGNATURE` - введенная вами
- `APATCH_CODE_SIGNATURE` - введенная вами
- `APATCH_PACKAGE_NAME` - me.bmax.apatch
- `APATCH_APP_CLASS` - APApplication
- `APATCH_SIGNATURE_METHOD` - verifyAppSignature

---

## 🚀 **Как использовать:**

### **Linux/macOS:**
```bash
# Сделайте исполняемым
chmod +x quick_add_extracted_secrets.sh

# Запустите
./quick_add_extracted_secrets.sh
```

### **Windows:**
```cmd
# Двойной клик по файлу или в cmd:
quick_add_extracted_secrets.bat
```

---

## 📝 **Пошаговое использование:**

### **1. Запустите скрипт**
Скрипт проверит GitHub CLI и авторизацию

### **2. Введите подписи**
```
APATCH_REAL_SIGNATURE: Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y=
APATCH_CODE_SIGNATURE: w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc=
```

### **3. Укажите репозиторий**
```
Репозиторий: AngelOfLlife/APatch
```

### **4. Подтвердите добавление**
```
Продолжить добавление секретов? (y/N): y
```

### **5. Дождитесь завершения**
```
✅ Успешно добавлено: 9/9 секретов
🎉 ВСЕ СЕКРЕТЫ ДОБАВЛЕНЫ УСПЕШНО!
```

---

## 🔑 **Приоритетные подписи для ввода:**

### **APATCH_REAL_SIGNATURE** (попробуйте по порядку):

#### **🥇 Вариант 1 - RSA сертификат** (самый вероятный):
```
Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y=
```

#### **🥈 Вариант 2 - Встроенная подпись:**
```
1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=
```

#### **🥉 Вариант 3 - Signature File:**
```
Sf8lTT4QszlGT6NOP8ltVuLmJpU=
```

### **APATCH_CODE_SIGNATURE:**

#### **🥇 Вариант 1 - SHA256 APK:**
```
w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc=
```

#### **🥈 Вариант 2 - SHA1 APK:**
```
CwsxhyPHS6AI0KQiw6TC7NE1Z4c=
```

---

## 📊 **Значения по умолчанию:**

Если просто нажать Enter, скрипт использует:
- **APATCH_REAL_SIGNATURE:** RSA сертификат
- **APATCH_CODE_SIGNATURE:** SHA256 APK
- **Репозиторий:** AngelOfLlife/APatch

---

## 🆘 **Требования:**

### **GitHub CLI:**
```bash
# Linux
sudo apt install gh

# macOS
brew install gh

# Windows
winget install GitHub.cli
```

### **Авторизация:**
```bash
gh auth login
```

---

## 🎯 **После добавления секретов:**

### **1. Перейдите в GitHub Actions:**
```
https://github.com/ваш-пользователь/APatch/actions
```

### **2. Запустите workflow:**
- `ultimate_fix_apatch_build.yml` (рекомендуется)
- `advanced_apatch_build.yml`
- `build_apatch_with_signature.yml`

### **3. Скачайте готовый APK:**
- Дождитесь завершения сборки (15-30 минут)
- Скачайте APK из раздела "Artifacts"
- Установите на устройство

### **4. Наслаждайтесь:**
- ✅ **Зависание исчезло**
- ✅ **APatch работает**
- ✅ **Root доступен**

---

## 💡 **Преимущества скрипта:**

- ⚡ **Быстро** - все секреты за 30 секунд
- 🔧 **Автоматически** - готовый keystore включен
- 🎯 **Точно** - использует извлеченные подписи
- 🛡️ **Безопасно** - прямо через GitHub CLI
- 🌐 **Альтернатива** - показывает ручной способ

---

## 🔄 **Если что-то пошло не так:**

### **Попробуйте другую подпись:**
1. Запустите скрипт еще раз
2. Введите Вариант 2 или 3 для APATCH_REAL_SIGNATURE
3. Запустите сборку снова

### **Ручное добавление:**
Скрипт всегда показывает как добавить секреты вручную через веб-интерфейс

---

**Скрипт делает весь процесс максимально простым и быстрым!** 🚀