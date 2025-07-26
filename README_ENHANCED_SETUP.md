# 🚀 Enhanced APatch Build - Обновленная настройка

## 📋 **Ключевые изменения**

### **✅ Что изменилось:**
- **❌ Больше НЕ НУЖНЫ** токены: `APATCH_REAL_SIGNATURE`, `APATCH_CODE_SIGNATURE`, `APATCH_PACKAGE_NAME`, `APATCH_APP_CLASS`, `APATCH_SIGNATURE_METHOD`
- **✨ Нужны ТОЛЬКО** секреты для подписи APK: `SIGNING_KEY`, `KEY_STORE_PASSWORD`, `KEY_PASSWORD`, `ALIAS`
- **🔧 Новый подход:** Универсальное патчирование кода вместо точечной замены

---

## 🛠️ **Доступные скрипты**

### **1. 🐍 Python (Рекомендуется)**

#### **`setup_enhanced_secrets.py` - All-in-One решение**
```bash
# Установить зависимости
pip install PyNaCl requests

# Установить токен
export GITHUB_TOKEN=your_token_here

# Запустить
python3 setup_enhanced_secrets.py
```

**Особенности:**
- ✅ Полная автоматизация
- ✅ Проверка всех требований
- ✅ Автоматическая генерация keystore
- ✅ Добавление всех секретов
- ✅ Очистка временных файлов

#### **`add_github_secrets_enhanced.py` - Ручная настройка**
```bash
pip install PyNaCl requests
export GITHUB_TOKEN=your_token_here
python3 add_github_secrets_enhanced.py
```

### **2. 🐚 Bash**

#### **`add_github_secrets_simple.sh` - Простое решение**
```bash
# Требования: gh CLI + Java JDK
export GITHUB_TOKEN=your_token_here
chmod +x add_github_secrets_simple.sh
./add_github_secrets_simple.sh
```

---

## 🔑 **Необходимые секреты**

| Секрет | Описание | Генерируется автоматически |
|--------|----------|---------------------------|
| `SIGNING_KEY` | Keystore в base64 | ✅ |
| `KEY_STORE_PASSWORD` | Пароль keystore | ✅ |
| `KEY_PASSWORD` | Пароль ключа | ✅ |
| `ALIAS` | Алиас ключа | ✅ |

**❌ НЕ НУЖНЫ:**
- ~~`APATCH_REAL_SIGNATURE`~~
- ~~`APATCH_CODE_SIGNATURE`~~
- ~~`APATCH_PACKAGE_NAME`~~
- ~~`APATCH_APP_CLASS`~~
- ~~`APATCH_SIGNATURE_METHOD`~~

---

## 🎯 **Как это работает**

### **🔄 Старый подход (токены замены):**
```yaml
# Искал конкретные строки и заменял их
- name: Replace signatures
  run: |
    find . -name "*.java" -exec sed -i 's/old_signature/new_signature/g' {} \;
```

### **✨ Новый подход (универсальное патчирование):**
```yaml
# Патчит все методы проверки подписи
- name: Bypass signature verification
  run: |
    # Найти все методы проверки подписи
    # Заменить их на dummy методы
    # Удалить все проверки сертификатов
    # Обойти все возможные защиты
```

---

## 🚀 **Пошаговая инструкция**

### **Шаг 1: Подготовка**
```bash
# Получить GitHub токен
# https://github.com/settings/tokens
# Права: repo, workflow

export GITHUB_TOKEN=ghp_xxxxxxxxxx
```

### **Шаг 2: Запуск (выберите один способ)**

#### **Вариант A: All-in-One (Рекомендуется)**
```bash
python3 setup_enhanced_secrets.py
```

#### **Вариант B: Bash**
```bash
./add_github_secrets_simple.sh
```

#### **Вариант C: Python расширенный**
```bash
python3 add_github_secrets_enhanced.py
```

### **Шаг 3: Проверка**
```bash
# Перейти в GitHub Actions
# https://github.com/AngelOfLlife/APatch/actions

# Найти workflow: "Enhanced APatch Build with Signature Bypass"
# Запустить вручную или создать новый тег
```

---

## 🔍 **Диагностика проблем**

### **❌ "GITHUB_TOKEN not found"**
```bash
export GITHUB_TOKEN=your_token_here
# Проверить права токена: repo, workflow
```

### **❌ "keytool not found"**
```bash
# Ubuntu/Debian
sudo apt install default-jdk

# macOS
brew install openjdk

# Windows
# Скачать Oracle JDK или OpenJDK
```

### **❌ "PyNaCl not found"**
```bash
pip install PyNaCl
# или
pip3 install PyNaCl
```

### **❌ "gh not found"**
```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# macOS
brew install gh
```

---

## ✅ **Ожидаемый результат**

После успешной настройки:

1. **🔐 Секреты добавлены** в GitHub репозиторий
2. **🏗️ Workflow готов** к запуску
3. **📱 APK будет собран** с обходом проверки подписи
4. **✨ Результат:** Полностью рабочий APatch без ограничений

---

## 🎯 **Следующие шаги**

1. **Запустить workflow:**
   - https://github.com/AngelOfLlife/APatch/actions
   - Найти "Enhanced APatch Build with Signature Bypass"
   - Нажать "Run workflow"

2. **Дождаться сборки** (~10-15 минут)

3. **Скачать APK** из Artifacts

4. **Установить** на устройство

5. **Наслаждаться** работающим APatch! 🎉