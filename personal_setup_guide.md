# 🎯 Персональная настройка для https://github.com/AngelOfLlife/APatch

## 🔗 Прямые ссылки для вашего репозитория

### 📊 Основные страницы:
- **Репозиторий**: https://github.com/AngelOfLlife/APatch
- **Настройки**: https://github.com/AngelOfLlife/APatch/settings
- **Секреты**: https://github.com/AngelOfLlife/APatch/settings/secrets/actions
- **Actions**: https://github.com/AngelOfLlife/APatch/actions

## 🔑 Добавление секретов

### Способ 1: GitHub CLI (Быстро)
```bash
# Авторизуйтесь в GitHub CLI
gh auth login

# Переключитесь на ваш репозиторий
cd /path/to/your/APatch
# или
gh repo clone AngelOfLlife/APatch && cd APatch

# Добавьте все секреты одной командой:
gh secret set SIGNING_KEY --body "MIIKpAIBAzCCCk4GCSqGSIb3DQEHAaCCCj8Eggo7MIIKNzCCBa4GCSqGSIb3DQEHAaCCBZ8EggWbMIIFlzCCBZMGCyqGSIb3DQEMCgECoIIFQDCCBTwwZgYJKoZIhvcNAQUNMFkwOAYJKoZIhvcNAQUMMCsEFEu8GkpJhgyNpLd4cRaHQMCNKzmpAgInEAIBIDAMBggqhkiG9w0CCQUAMB0GCWCGSAFlAwQBKgQQOAtcATLyibRqsQ0CimiE8wSCBNDKpWgEhTRZCDuEr1+WixrMVzvn/md6TW00fl7yiQXQu5chtBLSh1W6Yj5Fc9jZhW1I19tpa04r+FKaJfoATvx2GLzm3+Jbt6WaRhmqZ7CpLXyM5cQiBG+2IOHTViC24jBcXi5n7UeFTtMVq/eo4u0Y6FLq0usZJT6xbhXHv01jhuEgwg47BtkJ5UGkajpofai9AACexpQ9OshBxTEisXFHszNO1Qu/1DVDSiTBAGHWp/Df3XVuvHWjE4sz3FCo69OfUnlKdjm26vOkWCsN8Yac6YWCifSjQ9bnh7S1OIeyZwRzH2bP+F2QDq8OUeeg9JdyQsMs9tt60TNxOdNKTSymqSXgJ9trDMe4tI2hJYqfGtrIyTQeSe/7SlURUwzX9XiYyJh3XyB0ez+qRhzi+6iGtTIu4iuWx1AvLxLjGV5vlo3UUAs0Oifw4hVV5YwFV02C+Yb5Km/9d5CGKMezkev96yxINJhx0uX/2jZYqD+IvsH4R/KGuhKOftKw1JuK5rH6NfeVbN2tSX5PuxSRhCq8H+qfDDbx6ucJnUk3mS1BLEyGkWOqERPikh8UpBiUDWNgWUXulCOfeN08p9hoBx8bWgs1B9Kro2t4a0eFXFf/ZD0lQ7Ao0bf7ycK0XgRkoD3X7BJz3GwJJ+zYo9b02jUE18tykDrOHunPK7YviZ8d7j3okm6FHOnCDO4o7n2YGhparqSk22eRLlEi3ovSnsoyLPGjp6a3rVzwU+F0UbXg4hnD7UvIZW34cXeEv1dhr9GrqZ+i2FM+CC54iHUfZIMl6DCRr5UyTuprwve29PwnSk5MfaTxXw3QrMTQHTOOUZrB5kmU8hG3unuv9+DuzZ7twK/koiZMPrhJKRQDSiGoRIe6gxeZedihwgSvWg6vxo3zl7gz+WIdB97Q1YRtDF/+HSRTlHlV4dKhZtcQGUDdZlxq1EPDIZcnhjyMnCQeu4aJhGPq7wcLiR80GJeW5RPgJDYDPcQXbZf3SPmq+xT8gaLAGQx725Q58uxgqwt3Dj++aO7d9upttCRUu+oo+N3L1W23/izaTtj9R2m63bI6KEj5qcmV347+iOW9Rgih/pT+HMUFJMtOCmrOe+uTJZSNcweS5McFOkaBR/fqcj8mupI+gsszDcUIjUKoifoeAyEiaQ1eJtF/qB92zNSiOasm1UzoTSTT+2hTIpBvvtqL3nPz+nuQHJha+5sT7+GzBvG4IFMoGXJVnqlyx5KtFFhuduyn5HTGqmkBGYxTyna54c+t+LzyDhd7yf7cYI9ZIEl1afHQ2nBFChV6BQMQuBACQRvzQceCYoUWIlTL5mVM5sb0K/Q+rE/sU0JAYRfnJnF9adGudG8Vvdrmdt4hGtfi87FJFEzAf9hL7HBYaF9V4FCp7HAG8BksliFe5Z86V+f8HJ810ixnVnN1+QfbtS4LRmZCO38leqmnRojGKNN7bProp6zPeaY1Uv6iGHds8gozmc+PIvOiB0kJ9OiZ1APo/hcEaNsjkm0K6apA5xBwKSk2pD9MCxuZqzC8ebT3MPwTMYN5DzjvPqK9WXTJ9cRvR8j+z0ZAeopLBvsdOjXP3oBJSoGC6GJwlDIAu/Emo1IAQQtbz/i6jqh0zrctc3P2JNW2fl6Qkf0LypAL51lpXzFAMBsGCSqGSIb3DQEJFDEOHgwAYQBwAGEAdABjAGgwIQYJKoZIhvcNAQkVMRQEElRpbWUgMTc1MzI5MTE1MDI3NjCCBIEGCSqGSIb3DQEHBqCCBHIwggRuAgEAMIIEZwYJKoZIhvcNAQcBMGYGCSqGSIb3DQEFDTBZMDgGCSqGSIb3DQEFDDArBBRpkvbPTQa8vm4ceg2WP4e5bv1uhgICJxACASAwDAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEEIlh18CO+urFARBMXN9O38+AggPwlnGYfaaXH01gpdcCI9W413zZrepjjZQ8bvWpBncbtO5ZlCGAK+AUWXiYdNjHbd00keYlb+jMwN5024gqUq2O/kwIL0GeGRwv66n4gBIJovfdL/3iM/r33TUhj4VeKtjrfFOKNm30yHypPhwimi2FEfkFSFApYfGH5D+JRY79HIVTI2fFbcTx7OfCdzoBVEexDbiQ15BW+JCM0jSMFYZYDRyRq/ECP9K4baOqtWY+K3g0r+Z3CbCG49Mrigtev5tVpkF35Bam7zNKC5kyIDsRXOKzc3y/fjEqPlenThodiwRlDhu9HAoGJOG2HDoJ+GcBvQz3bbO37jKUYqj4eVTCIXBN1oddQwS0LBxyUkn+TkBwHjinG8T8hXQA3SpIGfv2sPDEOcTyEe/w36ElE9pl9+5cjNLsaDZyfMF1DRx1Q++KSb7CdQC3KnL1m2tZ4YPj21QW/z9nkFMnuarv8zbf2b4PzhFWGu2K6jf4T5iCVOOD5og40xEISZ0Co5aJpQ63sM1XNRO8akT4hq4v0DSZxszEouhedpNTL2nNNBFRaEs05N04hTqfTs1Kin9WAOb06bgiCyioLoSHRPFn7R7+XZQJjq9wR4BkQDI7mFCkpxsh29Grd4LQQk4rS5IZ4E5eiXTcN/QrSYYSOT+V2R7QIywaJ9kgyg/7KaPWzuCxVxMEJ4uu2jzWpnM24shFDpD6krjntrhBEpiJHmEE3EDEW3eX52RFH10qFW4d2V7UDjJas0G2xh4XgXhpvWFX6ADJIlxGgn5umeMU21srmISr8FWz0C6kfV0C8YbzzDbZ65bWU4XCVo/I0oiGwnNLxWEmlbUlzi9G5TTLlLWyoZqvwsP+RiYwlCTeK4wo8RjSMvcJFUQTRFy2MRLZUjVOAfNkW2CebHYwnqn7MOYTMoik5zavL3nOqxt6ah6ZvL4gKjQ/4v79FKe9hXR/jL7VC13BdMiObtgwZKhot8cJqN5v7BNT+W9Cyoha+jS1W/Yn9vveCGS5DecZeBRP8fhbPIEjiCb3RFIeH/rB7o4Zbh19cpSsxAwIIW/voOUGnZD/ifVELaSBn030xkMJnpnS7Xgm5i4pW38zYWGZHsM8WMAQKfhkdjKTWsKjNNc3Tuz9gxiAP/YU5sB1bfyvIFEao8BkQkJnEPutsJFAJht7slU5i/MveQ2YNJ+FKIf0wbfWg8t8DinyqS7mSI74icdcqvhSfd/GHNZxrAkHFzVC4S25ZYELJDbaS2wapk4P/YeAk3oyUmO3qCdqUcZw+YMGHivEOLgqQsODjIwczppbI+y0uE69MPyqrIVkeyLURsgpGUH4xcZ9rdk6k5+NQwshouygME0wMTANBglghkgBZQMEAgEFAAQgibQLR16AlnAJdQAEkTQ6pg4LmC7YVLPY/aRLAxgrMIAEFHdiKK7os/1YSb0LeKhBC+QasX/WAgInEA=="

gh secret set ALIAS --body "apatch"
gh secret set KEY_STORE_PASSWORD --body "apatch123"
gh secret set KEY_PASSWORD --body "apatch123"
gh secret set APATCH_ORIGINAL_SIGNATURE --body "1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk="
gh secret set APATCH_REAL_SIGNATURE --body "sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4="
gh secret set APATCH_PACKAGE_NAME --body "me.bmax.apatch"
gh secret set APATCH_APP_CLASS --body "APApplication"

echo "✅ Все секреты добавлены в AngelOfLlife/APatch!"
```

### Способ 2: Веб-интерфейс (Пошагово)

1. **Откройте страницу секретов**: https://github.com/AngelOfLlife/APatch/settings/secrets/actions

2. **Нажмите "New repository secret"**

3. **Добавьте каждый секрет**:

   | Name | Value |
   |------|-------|
   | `SIGNING_KEY` | `MIIKpAIBAzCCCk4GCSqGSIb3DQEHAaCCCj8Eggo7...` (длинная строка) |
   | `ALIAS` | `apatch` |
   | `KEY_STORE_PASSWORD` | `apatch123` |
   | `KEY_PASSWORD` | `apatch123` |
   | `APATCH_ORIGINAL_SIGNATURE` | `1x2twMoHvfWUODv7KkRRNKBzOfEqJwRKGzJpgaz18xk=` |
   | `APATCH_REAL_SIGNATURE` | `sypblYtJUCDSbk/u67zSBUyhRj+t7n6Tm6EPuEUnku4=` |
   | `APATCH_PACKAGE_NAME` | `me.bmax.apatch` |
   | `APATCH_APP_CLASS` | `APApplication` |

## 🚀 Добавление GitHub Actions Workflow

### Создайте файл workflow:

1. **Создайте папку** (если её нет): `.github/workflows/`

2. **Создайте файл**: `.github/workflows/build-apatch.yml`

3. **Скопируйте содержимое** из файла `build_apatch_with_signature.yml`

### Или через веб-интерфейс:

1. Перейдите: https://github.com/AngelOfLlife/APatch/actions
2. Нажмите "New workflow"
3. Выберите "set up a workflow yourself"
4. Вставьте содержимое workflow

## 🎯 План действий

### Шаг 1: Добавить секреты ✅
- [ ] SIGNING_KEY
- [ ] ALIAS  
- [ ] KEY_STORE_PASSWORD
- [ ] KEY_PASSWORD
- [ ] APATCH_ORIGINAL_SIGNATURE
- [ ] APATCH_REAL_SIGNATURE
- [ ] APATCH_PACKAGE_NAME
- [ ] APATCH_APP_CLASS

### Шаг 2: Добавить workflow
- [ ] Создать `.github/workflows/build-apatch.yml`
- [ ] Скопировать содержимое из готового файла

### Шаг 3: Запустить сборку
- [ ] Перейти в Actions: https://github.com/AngelOfLlife/APatch/actions
- [ ] Запустить "Build APatch with Correct Signature"
- [ ] Скачать готовый APK

## 💡 Полезные команды

### Проверить секреты (GitHub CLI):
```bash
gh secret list --repo AngelOfLlife/APatch
```

### Клонировать ваш репозиторий:
```bash
git clone https://github.com/AngelOfLlife/APatch.git
cd APatch
```

### Создать workflow файл локально:
```bash
mkdir -p .github/workflows
# Скопировать содержимое workflow в файл
cp build_apatch_with_signature.yml .github/workflows/build-apatch.yml
git add .github/workflows/build-apatch.yml
git commit -m "Add APatch build workflow"
git push
```

## 🔍 Проверка результата

После настройки:

1. **Секреты**: https://github.com/AngelOfLlife/APatch/settings/secrets/actions (должно быть 8 секретов)

2. **Actions**: https://github.com/AngelOfLlife/APatch/actions (должны появиться workflows)

3. **Запуск**: Нажать "Run workflow" → получить APK без зависания

## 🆘 Если нужна помощь

Если что-то не получается:
1. Проверьте права доступа к репозиторию
2. Убедитесь, что Actions включены
3. Проверьте правильность секретов
4. Посмотрите логи в Actions

Готов помочь на любом этапе! 🚀