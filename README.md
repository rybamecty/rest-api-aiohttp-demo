# Culture Analytics - Тестовое задание

REST API на aiohttp для тестового задания Junior-разработчика SaaS-сервиса.

## Структура проекта

```
culture-analytics/
├── server/              # Серверная часть на aiohttp
│   ├── app.py          # Основное приложение
│   ├── handlers.py     # HTTP обработчики
│   └── models.py       # Pydantic модели
├── client/             # Клиентская часть
│   ├── simple_client.py       # Ручной клиент
│   └── generated/             # Автосгенерированный клиент
├── tests/              # Тесты
│   ├── test_server.py         # Тесты сервера
│   └── test_simple_client.py  # Тесты клиента
├── openapi.yaml        # OpenAPI спецификация
├── requirements.txt    # Зависимости
└── pytest.ini          # Настройки pytest
```

## Установка

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Linux/Mac)
source venv/bin/activate

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

## Запуск сервера

```bash
python -m server.app
```

Сервер запустится на `http://localhost:8080`

## API Endpoints

- `GET /health` - Проверка работоспособности сервиса
- `POST /data` - Создать новый элемент данных
- `GET /data` - Получить список всех элементов
- `GET /data/{id}` - Получить элемент по ID
- `DELETE /data/{id}` - Удалить элемент по ID

## Примеры использования API

### Health check
```bash
curl http://localhost:8080/health
```

Ответ:
```json
{"status": "ok", "version": "1.0.0"}
```

### Создать элемент
```bash
curl -X POST http://localhost:8080/data \
  -H "Content-Type: application/json" \
  -d '{"name": "Продажи", "value": 1000.50}'
```

Ответ:
```json
{"id": 1, "name": "Продажи", "value": 1000.5}
```

### Получить все элементы
```bash
curl http://localhost:8080/data
```

### Получить элемент по ID
```bash
curl http://localhost:8080/data/1
```

### Удалить элемент
```bash
curl -X DELETE http://localhost:8080/data/1
```

## Использование клиента

### Простой клиент (ручной)

```python
from client.simple_client import CultureAnalyticsClient

# Создать клиент
client = CultureAnalyticsClient(base_url="http://localhost:8080")

# Проверить health
response = await client.health_check()
print(response)  # {'status': 'ok', 'version': '1.0.0'}

# Создать элемент
item = await client.create_data(name="Продажи", value=1000.50)
print(item)  # {'id': 1, 'name': 'Продажи', 'value': 1000.5}

# Получить список
items = await client.list_data()
print(items)
```

### Сгенерированный клиент (из OpenAPI)

```bash
# Установить генератор
pip install openapi-python-client

# Сгенерировать клиент
openapi-python-client generate --path openapi.yaml --output-path client/generated

# Установить сгенерированный клиент
pip install -e client/generated/
```

## Запуск тестов

```bash
# Запустить все тесты
pytest tests/ -v

# С покрытием кода
pytest tests/ -v --cov=server --cov-report=term-missing
```

## Выполненные требования

✅ **Реализован сервер на aiohttp**
- 5 endpoint'ов для работы с данными
- Валидация через Pydantic
- Обработка ошибок

✅ **Реализован клиент на aiohttp**
- Ручной клиент (`client/simple_client.py`)
- Автосгенерированный клиент (`client/generated/`)

✅ **Добавлена генерация контрактов OpenAPI**
- Полная спецификация API в `openapi.yaml`
- Описание всех endpoint'ов, параметров и ответов

✅ **Сгенерирован клиент из контрактов**
- Используется `openapi-python-client`
- Полная типизация и валидация

✅ **Написаны тесты**
- 6 тестов для сервера
- 4 теста для клиента
- Покрытие всех endpoint'ов и error-кейсов

## Технологический стек

- **aiohttp 3.9.5** - асинхронный веб-фреймворк для сервера и клиента
- **pydantic 2.5.0** - валидация и сериализация данных
- **pytest 7.4.3** - фреймворк для тестирования
- **pytest-aiohttp 1.0.5** - fixtures для тестирования aiohttp приложений
- **pytest-cov 4.1.0** - измерение покрытия кода тестами
- **openapi-python-client** - генератор Python клиента из OpenAPI спецификации

## Архитектурные решения

### Хранилище данных
Используется in-memory хранилище (dict) для упрощения тестового задания. В production следует использовать БД (PostgreSQL, MongoDB и т.д.).

### Валидация
Pydantic автоматически валидирует входящие данные и возвращает понятные ошибки при невалидных данных.

### Асинхронность
Использование async/await позволяет эффективно обрабатывать множество одновременных запросов.

### Тестирование
Покрытие тестами гарантирует корректность работы API и упрощает рефакторинг.

## Проверка кода

```bash
# Проверка стиля кода
flake8 server/ client/simple_client.py tests/

# Автоформатирование
black server/ client/simple_client.py tests/
```

## Возможные улучшения

- Добавить аутентификацию (JWT)
- Подключить базу данных (PostgreSQL + SQLAlchemy)
- Добавить пагинацию для `GET /data`
- Добавить фильтрацию и сортировку
- Добавить rate limiting
- Добавить логирование (structlog)
- Dockerize приложение
- Добавить CI/CD (GitHub Actions)

## Автор

Виктория Алексеенко
Email: vikkischastie@gmail.com
Telegram: @donnaViktoriia
