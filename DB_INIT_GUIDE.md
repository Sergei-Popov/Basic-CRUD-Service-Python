# Инициализация базы данных

## Автоматическое создание БД

Теперь при инициализации базы данных приложение автоматически:

1. **Проверяет существование базы данных** `crud_service`
2. **Создает её**, если она не существует (подключаясь к служебной БД `postgres`)
3. **Пересоздает все таблицы** в базе данных

## Как это работает

### Функция `ensure_database_exists()`

Эта функция выполняет следующие действия:

```python
async def ensure_database_exists() -> None:
    """Проверить существование БД и создать её при необходимости"""
    # 1. Подключается к служебной базе postgres
    # 2. Проверяет существование целевой БД через pg_database
    # 3. Создает БД, если она не существует
```

### Функция `init_db()`

Обновленная функция инициализации:

```python
async def init_db() -> None:
    """Пересоздать все таблицы в БД"""
    # 1. Вызывает ensure_database_exists()
    # 2. Удаляет все существующие таблицы
    # 3. Создает таблицы заново
```

## Использование

### Через API endpoint

Отправьте POST запрос на `/admin/init_db`:

```bash
curl -X POST http://localhost:4444/admin/init_db
```

Или через Swagger UI: http://localhost:4444/docs

### Программно

```python
from src.database.init_db import init_db

# Инициализация БД (создает БД если нужно + пересоздает таблицы)
await init_db()
```

### Только проверка/создание БД

```python
from src.database.init_db import ensure_database_exists

# Только создание БД без изменения таблиц
await ensure_database_exists()
```

## Тестирование

В проекте есть несколько тестовых скриптов:

### 1. Полная инициализация
```bash
python test_db_init.py
```

### 2. Создание новой БД
```bash
python test_create_db.py
```

### 3. Тест API endpoint
```bash
python test_api_init.py
```

## Конфигурация

Настройки подключения к PostgreSQL находятся в `src/config.py`:

```python
postgres_host: str = "localhost"
postgres_port: int = 5432
postgres_user: str = "postgres"
postgres_password: str = "1256"
postgres_db: str = "crud_service"
```

Или через переменные окружения в `.env` файле:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=crud_service
```

## Важные замечания

⚠️ **Внимание**: Функция `init_db()` **удаляет все существующие данные** в таблицах!

✅ Функция `ensure_database_exists()` безопасна - она только создает БД, если её нет, и не затрагивает существующие данные.

## Требования

- PostgreSQL должен быть запущен и доступен
- Пользователь должен иметь права на создание баз данных
- Для подключения к служебной БД `postgres` используются те же учетные данные

