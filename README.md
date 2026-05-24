# Кастомная система аутентификации и авторизации

Тестовое задание: https://nextcloud.effective-mobile.ru/s/9iZWAw3Xys8GMZZ?dir=/&openfile=true

## Стек

- Python 3.10
- Django
- Django REST Framework
- PostgreSQL
- JWT
- Docker
- Gunicorn

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone https://github.com/knasakin/custom_rbac.git
```

2. Перейти в директорию проекта:

```bash
cd custom_rbac
```

3. Создать `.env` файл в корне проекта по примеру `.env.example`

4. Запустить проект:

```bash
docker compose up --build
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000
```

Админка:

```text
http://127.0.0.1:8000/admin/
```

## Тестовые пользователи

При запуске проекта база данных автоматически заполняется ролями, бизнес-элементами, правилами доступа и тестовыми пользователями.

| Роль | Email | Пароль |
|---|---|---|
| admin | admin@admin.com | 1111 |
| manager | manager@manager.com | 2222 |
| user | user@user.com | 3333 |

## Seed-команда

Для заполнения базы данных используется management-команда:

```bash
python manage.py seed_data
```

## Аутентификация

В проекте реализована JWT-аутентификация

### Login

`POST /api/users/login/`

Пример запроса:

```json
{
    "email": "admin@admin.com",
    "password": "1111"
}
```

Пример ответа:

```json
{
    "token": "token_value"
}
```

Для доступа к защищённым endpoint'ам необходимо передавать JWT-токен в HTTP header:

```text
Authorization: Bearer <token_value>
```

JWT содержит:

- идентификатор пользователя
- время жизни токена
- уникальный идентификатор токена

После logout токен становится недействительным и больше не может использоваться.

### Регистрация пользователя

`POST /api/users/register/`

Пример запроса:

```json
{
    "email": "newuser@test.com",
    "name": "New User",
    "password": "1111",
    "password_repeat": "1111"
}
```

## API пользователей

```text
POST   /api/users/register/
POST   /api/users/login/
POST   /api/users/logout/
GET    /api/users/profile/
PATCH  /api/users/update/
DELETE /api/users/delete/
```

## Авторизация

В проекте реализована собственная RBAC-система доступа.

Структура доступа:

```text
User -> Role -> AccessRule -> BusinessElement
```

Роль пользователя определяет, какие действия он может выполнять с конкретными бизнес-элементами.

Поддерживаемые действия:

- `can_read`
- `can_create`
- `can_update`
- `can_delete`

Если пользователь не аутентифицирован, возвращается ошибка `401 Unauthorized`

Если пользователь аутентифицирован, но не имеет прав на ресурс, возвращается ошибка `403 Forbidden`

## API бизнес-элементов

Данные endpoint'ы используются для проверки работы RBAC-системы.

```text
GET    /api/access/products/
POST   /api/access/products/

GET    /api/access/orders/
POST   /api/access/orders/
```

Примеры:

- `user` может только просматривать `products` и `orders`
- `manager` может просматривать и создавать `products` и `orders`
- `admin` имеет полный доступ

## API управления правилами доступа

Правилами доступа может управлять пользователь с соответствующими правами.

```text
GET     /api/access/access-rules/
POST    /api/access/access-rules/
GET     /api/access/access-rules/{id}/
PATCH   /api/access/access-rules/{id}/
DELETE  /api/access/access-rules/{id}/
```

## Logout

`POST /api/users/logout/`

Logout реализован через инвалидизацию JWT-токена.

После logout уникальный идентификатор токена сохраняется в базе данных. При последующих запросах этот токен считается недействительным.

## Удаление пользователя

`DELETE /api/users/delete/`

Удаление пользователя реализовано так:

```text
is_active = False
```

Пользователь остаётся в базе данных, но больше не может залогиниться.
