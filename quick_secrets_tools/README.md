# 🔑 Quick Secrets Tools для APatch

## 📁 **Описание папки:**
Инструменты для быстрого и автоматического добавления всех необходимых секретов в GitHub репозиторий APatch.

---

## 🛠️ **Содержимое папки:**

### **📜 Скрипты добавления секретов:**
- **`quick_add_extracted_secrets.sh`** - Linux/macOS версия (bash)
- **`quick_add_extracted_secrets.bat`** - Windows версия (batch)

### **📚 Документация:**
- **`QUICK_SECRETS_GUIDE.md`** - Подробное руководство по использованию
- **`README.md`** - Этот файл

---

## ⚡ **Быстрый старт:**

### **🐧 Linux/macOS:**
```bash
cd quick_secrets_tools
chmod +x quick_add_extracted_secrets.sh
./quick_add_extracted_secrets.sh
```

### **🖥️ Windows:**
```cmd
cd quick_secrets_tools
quick_add_extracted_secrets.bat
```

---

## 🎯 **Что делают скрипты:**

### **✅ Автоматически добавляют 9 секретов:**
1. `SIGNING_KEY` - готовый keystore в base64
2. `ALIAS` - apatch
3. `KEY_STORE_PASSWORD` - apatch123
4. `KEY_PASSWORD` - apatch123
5. `APATCH_REAL_SIGNATURE` - ваша извлеченная подпись
6. `APATCH_CODE_SIGNATURE` - ваша извлеченная подпись
7. `APATCH_PACKAGE_NAME` - me.bmax.apatch
8. `APATCH_APP_CLASS` - APApplication
9. `APATCH_SIGNATURE_METHOD` - verifyAppSignature

### **✅ Умные значения по умолчанию:**
- **APATCH_REAL_SIGNATURE:** `Uo6uAtr8EUXCnfCGs2ooeo3qJ9Y=` (RSA сертификат)
- **APATCH_CODE_SIGNATURE:** `w/FIHwoT4GORX42073W/q7jHzjgc5Zo+8EkPwFkY9Mc=` (SHA256 APK)
- **Репозиторий:** `AngelOfLlife/APatch`

---

## 📋 **Требования:**

### **GitHub CLI установлен:**
```bash
# Linux
sudo apt install gh

# macOS
brew install gh

# Windows
winget install GitHub.cli
```

### **GitHub CLI авторизован:**
```bash
gh auth login
```

---

## 🚀 **Типичный процесс использования:**

### **1. Извлеките подписи (из других папок):**
```bash
# Windows
../windows_tools/windows_quick_extract.py APatch.apk

# Linux
../quick_extract_apk_signatures.py APatch.apk
```

### **2. Запустите скрипт добавления секретов:**
```bash
# Linux/macOS
./quick_add_extracted_secrets.sh

# Windows
quick_add_extracted_secrets.bat
```

### **3. Следуйте инструкциям скрипта:**
- Введите извлеченные подписи (или используйте по умолчанию)
- Укажите репозиторий
- Подтвердите добавление

### **4. Запустите GitHub Actions:**
- Перейдите в Actions репозитория
- Запустите `ultimate_fix_apatch_build.yml`
- Дождитесь сборки и скачайте APK

---

## 💡 **Преимущества:**

### **⚡ Скорость:**
- **30 секунд** от запуска до готовых секретов
- **Минимум ввода** - большинство значений по умолчанию

### **🎯 Точность:**
- **Готовый keystore** уже включен в скрипт
- **Проверенные подписи** из оригинального APK
- **Автоматическая проверка** GitHub CLI и репозитория

### **🔒 Безопасность:**
- **Прямое взаимодействие** с GitHub API
- **Локальное выполнение** без передачи данных третьим лицам
- **Возможность проверки** кода скриптов

### **🌐 Универсальность:**
- **Кроссплатформенность** - Linux, macOS, Windows
- **Альтернативные способы** - ручное добавление через веб-интерфейс
- **Подробная документация** с примерами

---

## 🆘 **Устранение проблем:**

### **GitHub CLI не найден:**
```bash
# Установите GitHub CLI
# Linux: sudo apt install gh
# macOS: brew install gh  
# Windows: winget install GitHub.cli
```

### **GitHub CLI не авторизован:**
```bash
gh auth login
# Следуйте инструкциям для входа
```

### **Нет доступа к репозиторию:**
- Проверьте правильность имени репозитория
- Убедитесь, что у вас есть права на запись
- Проверьте авторизацию в GitHub CLI

### **Некоторые секреты не добавились:**
- Скрипт покажет альтернативный способ через веб-интерфейс
- Можете добавить вручную через GitHub Settings

---

## 📖 **Дополнительная документация:**

### **Подробное руководство:**
- Откройте `QUICK_SECRETS_GUIDE.md` для детального описания

### **Другие инструменты:**
- `../windows_tools/` - инструменты для Windows
- `../SOLUTION_GUIDE.md` - общее руководство по решению
- `../ultimate_fix_apatch_build.yml` - рекомендуемый workflow

---

## 🎉 **Результат:**

**После использования этих инструментов у вас будет полностью настроенный GitHub репозиторий, готовый для автоматической сборки APatch без зависания!**

### **✅ Все секреты добавлены**
### **✅ Готовый keystore включен** 
### **✅ Правильные подписи настроены**
### **✅ Можно запускать GitHub Actions**

---

**🚀 Самый быстрый способ решить проблему зависания APatch!**