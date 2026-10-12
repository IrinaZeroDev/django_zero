"""Telegram-бот — клиент Django API.

Бот не является частью Django: он отдельной программой отправляет
HTTP-запросы к API (/api/register/, /api/user/<id>/) и пересылает
ответы пользователю.

Запуск (сервер Django должен быть уже запущен):
    python bot_main.py
"""
import os
from datetime import datetime
from pathlib import Path

import requests
import telebot
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/api').rstrip('/')
REQUEST_TIMEOUT = 10  # секунд

SERVER_UNAVAILABLE = 'Сервер сейчас недоступен, попробуйте позже.'
UNEXPECTED_ERROR = 'Непредвиденная ошибка. Попробуйте позже.'


def register(user_id, username, api_url=API_URL):
    """Регистрирует пользователя через API и возвращает текст ответа."""
    try:
        response = requests.post(
            f'{api_url}/register/',
            json={'user_id': user_id, 'username': username},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return SERVER_UNAVAILABLE

    if response.status_code == 201:
        number = response.json()['id']
        return f'Вы успешно зарегистрированы! Ваш номер: {number}'
    if response.status_code == 200:
        return 'Вы уже были зарегистрированы ранее.'
    return 'Произошла ошибка при регистрации.'


def my_info(user_id, api_url=API_URL):
    """Запрашивает данные пользователя через API и возвращает текст."""
    try:
        response = requests.get(
            f'{api_url}/user/{user_id}/', timeout=REQUEST_TIMEOUT
        )
    except requests.RequestException:
        return SERVER_UNAVAILABLE

    if response.status_code == 404:
        return 'Вы не зарегистрированы. Отправьте /start.'
    if response.status_code != 200:
        return UNEXPECTED_ERROR

    data = response.json()
    created = datetime.fromisoformat(data['created_at'])
    username = f"@{data['username']}" if data['username'] else 'не указано'
    return (
        'Ваша регистрация:\n'
        f"Номер: {data['id']}\n"
        f"ID в Telegram: {data['user_id']}\n"
        f'Имя пользователя: {username}\n'
        f'Дата регистрации: {created:%d.%m.%Y %H:%M}'
    )


def create_bot(token, api_url=API_URL, threaded=True):
    """Создаёт бота и подключает обработчики команд."""
    bot = telebot.TeleBot(token, threaded=threaded)

    @bot.message_handler(commands=['start'])
    def start_command(message):
        user = message.from_user
        bot.send_message(
            message.chat.id, register(user.id, user.username, api_url)
        )

    @bot.message_handler(commands=['myinfo'])
    def myinfo_command(message):
        bot.reply_to(message, my_info(message.from_user.id, api_url))

    return bot


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise SystemExit(
            'Не задан TELEGRAM_BOT_TOKEN: впишите токен от @BotFather в .env'
        )
    print(f'Бот запущен, API: {API_URL}')
    create_bot(token).infinity_polling()


if __name__ == '__main__':
    main()
