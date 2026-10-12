# django_zero
мои домашние задания в курсе темы "Веб-разработка с использованием Django" в курсе "Программист на Python с нуля с помощью ChatGPT"

## DJ06. Архитектура Django: создание приложений и их взаимодействие

### [Задание](./DJ06/mysite)
Повторить действия за преподавателем: проект `mysite` с отдельными приложениями, связи между ними без циклических импортов, секреты в `.env`.

Что сделано:
- проект `mysite` (`django-admin startproject mysite`), приложения `users` и `orders` (`startapp`), оба в `INSTALLED_APPS`;
- `users`: модель `User` на основе `AbstractUser` (уникальный email, адрес), `AUTH_USER_MODEL = 'users.User'`, страницы `login/` и `register/`;
- `orders`: модель `Order` (товар, цена) со связью `ForeignKey` на пользователя через `settings.AUTH_USER_MODEL`, `related_name='orders'`, страница `orders/user/<id>/`, где пользователь берётся через `get_user_model()`;
- приложения не импортируют друг друга, циклических импортов нет;
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `TELEGRAM_BOT_TOKEN` читаются из `.env` через `python-dotenv`; `.env` не хранится в git, образец — `.env.example`.

Запуск:
```
cd DJ06/mysite
pip install -r requirements.txt
copy .env.example .env      # и вписать DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver
```
Тесты: `python manage.py test`
