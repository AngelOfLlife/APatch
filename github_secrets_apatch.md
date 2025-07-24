# GitHub Secrets для APatch

## Секреты для добавления в GitHub Repository Settings > Secrets and variables > Actions

### Основная подпись APatch
```
Name: APATCH_ORIGINAL_SIGNATURE
Value: 1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=
```

### Дополнительная информация для CI/CD

```
Name: APATCH_PACKAGE_NAME
Value: me.bmax.apatch
```

```
Name: APATCH_APP_CLASS
Value: APApplication
```

```
Name: APATCH_SIGNATURE_METHOD
Value: verifyAppSignature
```

## Использование в GitHub Actions

Пример использования в workflow файле (`.github/workflows/build.yml`):

```yaml
name: Build APatch
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup variables
        run: |
          echo "ORIGINAL_SIGNATURE=${{ secrets.APATCH_ORIGINAL_SIGNATURE }}" >> $GITHUB_ENV
          echo "PACKAGE_NAME=${{ secrets.APATCH_PACKAGE_NAME }}" >> $GITHUB_ENV
          
      - name: Verify signature
        run: |
          echo "Original signature: $ORIGINAL_SIGNATURE"
          # Ваш код для работы с подписью
```

## Команды для добавления секретов через GitHub CLI

```bash
# Установить GitHub CLI если не установлен
# brew install gh  # macOS
# sudo apt install gh  # Ubuntu

# Авторизоваться
gh auth login

# Добавить секреты
gh secret set APATCH_ORIGINAL_SIGNATURE --body "1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
gh secret set APATCH_PACKAGE_NAME --body "me.bmax.apatch"
gh secret set APATCH_APP_CLASS --body "APApplication"
gh secret set APATCH_SIGNATURE_METHOD --body "verifyAppSignature"
```

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте секреты в код
- Используйте эти секреты только в приватных репозиториях
- Проверьте права доступа к секретам
- Секреты видны только в workflow логах при явном выводе

## Альтернативные форматы

### Для Environment Variables:
```bash
export APATCH_ORIGINAL_SIGNATURE="1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
export APATCH_PACKAGE_NAME="me.bmax.apatch"
```

### Для Docker:
```dockerfile
ARG APATCH_ORIGINAL_SIGNATURE
ENV APATCH_SIGNATURE=${APATCH_ORIGINAL_SIGNATURE}
```