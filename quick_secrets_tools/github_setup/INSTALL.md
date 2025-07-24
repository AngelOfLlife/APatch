# 🚀 Инструкция по установке GitHub CLI

## 📋 **Ваши данные для настройки:**

- **Пользователь:** `AngelOfLlife`
- **Репозиторий:** `AngelOfLlife/APatch`
- **Токен:** `ваш_github_токен_здесь`

---

## ⚡ **Быстрая установка:**

### **🖥️ Windows:**
```cmd
cd quick_secrets_tools\github_setup

# 1. Настройка токена
setup_token_simple.bat
# Введите: ваш_github_токен_здесь

# 2. Установка GitHub CLI
install_github_cli.bat

# 3. Авторизация
auth_github_cli.bat
```

### **🐧 Linux/macOS:**
```bash
cd quick_secrets_tools/github_setup

# 1. Настройка токена
chmod +x *.sh
./setup_token_simple.sh
# Введите: ваш_github_токен_здесь

# 2. Установка GitHub CLI
./install_github_cli.sh

# 3. Авторизация
./auth_github_cli.sh
```

---

## 📝 **Пошаговое руководство:**

### **Шаг 1: Настройка токена**
Запустите скрипт для вашей ОС и введите токен когда будет запрошено

### **Шаг 2: Установка GitHub CLI**
Запустите установочный скрипт - он автоматически определит вашу ОС

### **Шаг 3: Авторизация**
Выберите способ авторизации (рекомендуется через токен для быстроты)

### **Шаг 4: Добавление секретов**
```bash
cd .. 
# Windows: quick_add_extracted_secrets.bat
# Linux/macOS: ./quick_add_extracted_secrets.sh
```

---

## 🎯 **После установки:**

✅ GitHub CLI настроен и авторизован  
✅ Готов к добавлению секретов в репозиторий  
✅ Готов к запуску GitHub Actions сборки  

---

**⚠️ Важно: Сохраните этот файл локально, так как он содержит ваш персональный токен!**