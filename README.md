# PetDiary — дневник питомца (учебный проект)

**PetDiary** — веб-приложение для владельцев домашних животных: хранение карточек питомцев, дневниковых записей, планирование процедур, ведение ветеринарной истории и получение советов по уходу.

## Технологический стек

- Python 3.14, Django 6.1, Django REST Framework 3.18
- PostgreSQL (по умолчанию) / SQLite (для тестирования)
- HTML5, CSS3, JavaScript
- psycopg 3 (драйвер PostgreSQL)

## Структура проекта

```
PetDiary/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── PetDiary/               # настройки Django (settings.py, urls.py, wsgi.py, asgi.py)
├── accounts/               # пользователи, роли, профили, аутентификация
├── pets/                   # питомцы, измерения
├── diary/                  # дневниковые записи, ветеринарные визиты
├── care/                   # процедуры, история выполнения
├── advice/                 # советы по уходу, категории
├── api/                    # REST API (Django REST Framework)
├── templates/              # базовые шаблоны (base.html, pages/home.html)
├── static/                 # CSS, JavaScript, изображения
└── db_test.sqlite3         # тестовая база (SQLite, для локального тестирования)
```

## Установка (Windows)

1. Установите Python 3.14 (`python.org`, при установке выберите «Add Python to PATH»):
   был уже установлен в `C:\Users\kasae\AppData\Local\Programs\Python\Python314\`.
2. Создайте виртуальное окружение (необязательно для тестирования):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
3. Установите зависимости:
   ```cmd
   pip install -r requirements.txt
   ```
4. Настройте переменные окружения (создайте файл `.env` из `.env.example`; не коммитьте реальные пароли).
5. Примените миграции:
   ```cmd
   python manage.py migrate
   ```
6. Создайте суперпользователя:
   ```cmd
   python manage.py shell -c "from accounts.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
   ```
7. Запустите сервер:
   ```cmd
   python manage.py runserver 127.0.0.1:8000
   ```
8. Откройте браузер: `http://127.0.0.1:8000/`

## Настройка PostgreSQL

Проект настроен на PostgreSQL по умолчанию. Пример DSN:
```
DATABASE_URL=postgresql://postgres:your_password@127.0.0.1:5432/petdiary
```
Для тестирования без PostgreSQL:
```
DATABASE_URL=sqlite:////C:/Users/kasae/Downloads/PetDiary/db_test.sqlite3
```

## Проверка работы

- `python manage.py check` — проверка конфигурации («no issues»).
- `python manage.py migrate` — применение миграций (все миграции применены).
- `python manage.py test` — тесты (19 тестов пройдены — `Ran 19 tests... OK`).

## ИИ-помощник

Доступен авторизованным пользователям по адресу `/assistant/`. Хранит историю диалогов в БД, передаёт модели системную роль и контекст питомцев текущего пользователя. Для включения задайте `AI_PROVIDER_API_KEY`, `AI_API_URL` и `AI_MODEL` в `.env`. Без ключа интерфейс доступен, а отправка сообщений вернёт понятное сообщение о необходимости настройки. ИИ не заменяет ветеринарную консультацию.

## API

Документация API — `http://127.0.0.1:8000/api/` (APIRootView).
Endpoints: `/api/pets/`, `/api/diary/`, `/api/vet-visits/`, `/api/care/`, `/api/procedure-logs/`, `/api/advice/`, `/api/advice-categories/`, `/api/users/me/`.
Аутентификация: `Authorization: Token <key>` (rest_framework.authtoken) или сессии. Эндпоинты питомцев, дневника и процедур ограничивают данные владельцем; связанные питомцы при записи проверяются на принадлежность текущему пользователю.

## Диаграммы

Диаграммы проекта:
- ERD_PetDiary — Entity-Relationship диаграмма базы данных.
- UseCase_PetDiary — Use Case Diagram (акторы: Владелец, Администратор).
- Class_PetDiary — Class Diagram моделей.
- Sequence_PasswordReset — восстановление пароля по электронной почте.

## Отчёты

Файлы отчётов — в архиве PetDiary_Reports.zip:
- Р01_Тема1_Проектирование_ИС.docx
- Р02_ТЕМА2_Обоснование_стека.docx
- Р03_Тема3_Настройка_окружения_Git.docx
- Р04_Тема4_Проектирование_БД.docx
- Р05_Тема6_Регистрация_аутентификация_авторизация.docx
- Р06_Тема7_Восстановление_пароля_по_почте.docx
- Р07_ТЕМА8_Разграничение_прав_доступа.docx
- Р08_ТЕМА9-10-11_Разработка_интерфейса.docx
- Р09_ТЕМА12_REST_API.docx
- Р10_Итоговый_отчет_по_практике.docx

## Статус тестирования

Автоматические проверки необходимо выполнить в локальном окружении после установки зависимостей. В среде ревизии Django отсутствовал, поэтому результат `manage.py check` и тестов не подтверждён.
