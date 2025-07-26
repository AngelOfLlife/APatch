# 🔧 GitHub CLI Setup Tools

## 📁 **Описание:**
Автоматические инструменты для настройки GitHub CLI и токена авторизации.

---

## 🛠️ **Файлы:**

- **`setup_token.bat`** - Windows: настройка токена
- **`auth_github_cli.bat`** - Windows: авторизация GitHub CLI
- **`INSTALL.md`** - Подробные инструкции по установке

---

## ⚡ **Быстрый старт:**

### **Windows:**
```cmd
cd quick_secrets_tools\github_setup

# 1. Настройте токен
setup_token.bat

# 2. Авторизация (после установки GitHub CLI)
auth_github_cli.bat
```

---

## 📋 **Данные для настройки:**

- **Пользователь:** `AngelOfLlife`
- **Репозиторий:** `AngelOfLlife/APatch`
- **Токен:** см. файл `INSTALL.md` или создайте свой в GitHub Settings

---

## 🔑 **Как получить токен:**

1. Перейдите в GitHub.com → Settings → Developer settings → Personal access tokens
2. Создайте новый token с правами `repo`, `write:packages`, `delete:packages`
3. Скопируйте токен и используйте в скриптах

---

**🚀 После настройки переходите к добавлению секретов в репозиторий!**