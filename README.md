# Avito API Клиент

Библиотека для удобной работы с API Авито для бизнеса. Поддерживает работу с множеством аккаунтов и управление токенами авторизации.

## Особенности

* 🚀 Простая и удобная интеграция с API Авито
* 🔑 Полная поддержка OAuth 2.0 аутентификации (client_credentials и refresh_token)
* 💾 Возможность использования сохранённых токенов из базы данных
* 🔄 Автоматическое обновление токенов при истечении срока действия
* ✅ Проверка валидности токенов при инициализации через тестовый запрос
* 📦 Поддержка всех основных методов API Авито
* 🛠 Детальная обработка ошибок и логирование

## Установка

```bash
pip install "git+https://github.com/vukeep/avito.git"
```

## Быстрый старт

### Базовое использование

```python
from avito_api import AvitoAPIClient

# Инициализация клиента с учетными данными
client = AvitoAPIClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Получение информации о пользователе
user_info = client.user.get_user_info()
print(user_info)

# Получение сообщений из мессенджера
messages = client.messenger.get_chats(user_id=12345, limit=10)
print(messages)
```

### Использование с сохраненными токенами

```python
from avito_api import AvitoAPIClient

# Инициализация с существующим токеном
# При инициализации библиотека проверит валидность токена через запрос к API
client = AvitoAPIClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    access_token="SAVED_ACCESS_TOKEN",
    refresh_token="SAVED_REFRESH_TOKEN",
    token_expires_at=1680000000  # timestamp когда истекает токен
)

# Проверяем, был ли токен обновлен при инициализации
if client.was_token_refreshed():
    print("Токен был обновлен при инициализации")
    # Сохраняем обновленные токены
    token_info = client.get_token_info()
    database.save_tokens(shop_id, token_info)

# Выполнение запроса - токен обновится автоматически при необходимости
chats = client.messenger.get_chats(user_id=12345)
```

## Автоматическая проверка и обновление токенов

Библиотека реализует несколько уровней проверки токенов:

1. **При инициализации** - Если передан `access_token`, будет выполнен тестовый запрос к API для проверки его валидности
2. **Перед запросами** - Проверка времени истечения токена перед каждым запросом
3. **При ошибке авторизации** - Автоматическая попытка обновить токен и повторить запрос

```python
# Пример проверки статуса токена после инициализации
client = AvitoAPIClient(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    access_token="POSSIBLY_INVALID_TOKEN",
    refresh_token="REFRESH_TOKEN"
)

# Проверяем, был ли токен обновлен
if client.was_token_refreshed():
    print("Токен был невалиден и был автоматически обновлен")
    # Получаем новую информацию о токенах для сохранения
    token_info = client.get_token_info()
else:
    print("Токен был валиден, обновление не требовалось")
```

## Основные компоненты API

Библиотека разделена на несколько модулей для удобной работы с различными типами API:

* `client.user` - доступ к информации о пользователе
* `client.item` - работа с объявлениями
* `client.messenger` - взаимодействие с сообщениями
* `client.services` - применение услуг и продвижение
* `client.autoload` - работа с автозагрузкой

## Пример работы с множеством аккаунтов

Для проектов, где необходимо работать с несколькими аккаунтами Авито, библиотека предоставляет удобный механизм управления токенами:

```python
# Получаем данные из БД или другого хранилища
saved_tokens = database.get_tokens(shop_id)

# Инициализируем клиент с этими данными
client = AvitoAPIClient(
    client_id=saved_tokens["client_id"],
    client_secret=saved_tokens["client_secret"],
    access_token=saved_tokens["access_token"],
    refresh_token=saved_tokens["refresh_token"],
    token_expires_at=saved_tokens["token_expires_at"]
)

# Если токен был обновлен при инициализации, сохраняем
if client.was_token_refreshed():
    token_info = client.get_token_info()
    database.save_tokens(shop_id, token_info)

# Выполняем запрос к API
result = client.item.get_items()

# После выполнения запросов проверяем, не обновился ли токен
new_token_info = client.get_token_info()
if new_token_info["token_expires_at"] != saved_tokens["token_expires_at"]:
    database.save_tokens(shop_id, new_token_info)
```

## Логирование

Библиотека имеет встроенное логирование через стандартный модуль `logging`:

```python
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
avito_logger = logging.getLogger('avito_api')
avito_logger.setLevel(logging.DEBUG)  # Для подробного вывода работы с токенами
```

## Документация API

Полную документацию по API Авито можно найти на [официальном сайте разработчиков](https://developers.avito.ru/).

## Требования

* Python 3.7+
* Requests

## Примеры

В репозитории есть несколько примеров использования библиотеки:

* `example_multi_account.py` - работа с несколькими аккаунтами
* `example_auth_flow.py` - пример OAuth авторизации
* `example_token_validation.py` - проверка и обновление токенов

## Лицензия

MIT 
