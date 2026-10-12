# django_zero
мои домашние задания в курсе темы "Веб-разработка с использованием Django" в курсе "Программист на Python с нуля с помощью ChatGPT"

**Стек:** Python 3, Django 5, Django REST Framework, SQLite, Bootstrap 5, aiogram / pyTelegramBotAPI.

Каждый урок — в своей ветке: ветка содержит проект урока и все предыдущие. В таблице — ссылка на ветку и папку проекта.

| Урок | Тема | Что сделано | Код |
|---|---|---|---|
| DJ01 | Введение в Django и создание проекта | Приложение со страницами `data` и `test` | [main → pythonProjectweb](./pythonProjectweb) |
| DJ02 | Шаблоны | Меню и подвал через `include`, 4 страницы на Bootstrap | [ветка DJ02](https://github.com/IrinaZeroDev/django_zero/tree/DJ02/webDjango) |
| DJ03 | Модели | Новостной сайт: модель новости с автором, вывод полной информации | [ветка DJ03](https://github.com/IrinaZeroDev/django_zero/tree/DJ03/webDjango) |
| DJ04 | Формы и развёртывание | Каталог фильмов: добавление через форму, список фильмов | [ветка DJ04](https://github.com/IrinaZeroDev/django_zero/tree/DJ04/movie_project) |
| DJ05 | Аутентификация | Регистрация, вход, выход, редактирование профиля; кастомная модель пользователя | [ветка DJ05](https://github.com/IrinaZeroDev/django_zero/tree/DJ05/DJ05/auth_test_hw) |
| DJ06 | Архитектура: взаимодействие приложений | Приложения пользователей и заказов, связь моделей, настройки в `.env` | [ветка DJ06](https://github.com/IrinaZeroDev/django_zero/tree/DJ06/DJ06/mysite) |
| DJ07 | Интеграция Django с Telegram-ботом | REST API на DRF для регистрации пользователей бота, CORS, бот на pyTelegramBotAPI | [ветка DJ07](https://github.com/IrinaZeroDev/django_zero/tree/DJ07/DJ07/djangobot) |

Подробное условие и инструкция запуска — в README соответствующей ветки.

## Как запустить проект урока

```bash
git clone https://github.com/IrinaZeroDev/django_zero.git
cd django_zero
git checkout DJ07                # нужная ветка
cd DJ07/djangobot                # папка проекта из таблицы
pip install -r requirements.txt
copy .env.example .env         # если в папке есть .env.example — вписать свои значения
python manage.py migrate
python manage.py runserver
```

## DJ01. Введение в Django и создание проекта

### [Задание](./pythonProjectweb)

Создайте новое Django приложение, зарегистрируйте его и сделайте так чтоб при переходе на страницу data и test открывались страницы с разным содержимым.
