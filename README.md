# django_zero
мои домашние задания в курсе темы "Веб-разработка с использованием Django" в курсе "Программист на Python с нуля с помощью ChatGPT"

## DJ07. Интеграция Django с телеграм-ботом

### [Задание](./DJ07/djangobot)
Выполнены все три уровня задания в одном проекте `djangobot`.

**Задание 1 (лёгкий уровень).** Проект с приложением `bot`, Django REST Framework, модель `TelegramUser` (ID в Telegram и имя пользователя), сериализатор, endpoint `POST /api/register/` с JSON-ответом.

**Задание 2 (средний уровень).** Telegram-бот на `telebot` (`bot_main.py`): команда `/start` передаёт в API ID и username и сообщает пользователю о регистрации.

**Задание 3 (продвинутый уровень).** Endpoint `GET /api/user/<id>/`, команда бота `/myinfo`, обработка ошибок (не зарегистрирован, сервер недоступен), CORS через `django-cors-headers` со списком разрешённых доменов.

Бот — отдельный клиент, а не часть Django: он обращается к API по HTTP.

| Метод и адрес | Ответ |
|---|---|
| `POST /api/register/` `{"user_id": 123, "username": "name"}` | 201 — зарегистрирован, 200 — уже был, 400 — неверные данные |
| `GET /api/user/<user_id>/` | 200 — данные пользователя, 404 — не найден |

Запуск:
```
cd DJ07/djangobot
pip install -r requirements.txt
copy .env.example .env      # вписать DJANGO_SECRET_KEY и TELEGRAM_BOT_TOKEN
python manage.py migrate
python manage.py runserver  # терминал 1
python bot_main.py          # терминал 2
```
Тесты: `python manage.py test`
