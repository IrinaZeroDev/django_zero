from unittest import mock

from django.test import LiveServerTestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from telebot import types

import bot_main

from .models import TelegramUser


class RegisterApiTests(APITestCase):
    url = reverse('register_user')

    def test_new_user_created_with_201(self):
        response = self.client.post(
            self.url, {'user_id': 123456789, 'username': 'murka'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user_id'], 123456789)
        self.assertEqual(response.data['username'], 'murka')
        self.assertIn('created_at', response.data)

    def test_repeat_registration_returns_200(self):
        TelegramUser.objects.create(user_id=1, username='murka')
        response = self.client.post(
            self.url, {'user_id': 1, 'username': 'murka'}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)
        self.assertEqual(TelegramUser.objects.count(), 1)

    def test_user_without_username(self):
        response = self.client.post(
            self.url, {'user_id': 5, 'username': None}, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TelegramUser.objects.get().username, '')

    def test_missing_or_wrong_user_id_gives_400(self):
        for body in ({}, {'user_id': 'abc'}, {'user_id': -1}):
            response = self.client.post(self.url, body, format='json')
            self.assertEqual(response.status_code, 400, body)
        self.assertFalse(TelegramUser.objects.exists())

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class UserInfoApiTests(APITestCase):
    def test_existing_user(self):
        TelegramUser.objects.create(user_id=42, username='barsik')
        response = self.client.get(reverse('user_info', args=[42]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'barsik')

    def test_unknown_user_gives_404(self):
        response = self.client.get(reverse('user_info', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.data)


@override_settings(CORS_ALLOWED_ORIGINS=['https://shop.example.com'])
class CorsTests(APITestCase):
    def test_allowed_origin_gets_cors_header(self):
        response = self.client.get(
            reverse('user_info', args=[1]),
            HTTP_ORIGIN='https://shop.example.com',
        )
        self.assertEqual(
            response.headers['Access-Control-Allow-Origin'],
            'https://shop.example.com',
        )

    def test_other_origin_gets_no_cors_header(self):
        response = self.client.get(
            reverse('user_info', args=[1]),
            HTTP_ORIGIN='https://evil.example.com',
        )
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)


class BotWithLiveApiTests(LiveServerTestCase):
    """Функции бота работают с настоящим запущенным API."""

    def setUp(self):
        self.api_url = f'{self.live_server_url}/api'

    def test_start_then_myinfo(self):
        self.assertEqual(
            bot_main.my_info(777, self.api_url),
            'Вы не зарегистрированы. Отправьте /start.',
        )
        first = bot_main.register(777, 'murka', self.api_url)
        self.assertTrue(first.startswith('Вы успешно зарегистрированы!'))
        self.assertEqual(
            bot_main.register(777, 'murka', self.api_url),
            'Вы уже были зарегистрированы ранее.',
        )
        info = bot_main.my_info(777, self.api_url)
        self.assertIn('ID в Telegram: 777', info)
        self.assertIn('Имя пользователя: @murka', info)

    def test_server_down_message(self):
        dead_url = 'http://127.0.0.1:9/api'
        self.assertEqual(
            bot_main.register(1, 'x', dead_url), bot_main.SERVER_UNAVAILABLE
        )
        self.assertEqual(
            bot_main.my_info(1, dead_url), bot_main.SERVER_UNAVAILABLE
        )


class BotHandlersTests(LiveServerTestCase):
    """Команды /start и /myinfo вызывают нужные ответы бота."""

    def make_update(self, text, update_id):
        return types.Update.de_json({
            'update_id': update_id,
            'message': {
                'message_id': update_id,
                'date': 0,
                'chat': {'id': 555, 'type': 'private'},
                'from': {'id': 555, 'is_bot': False, 'first_name': 'Ира',
                         'username': 'irina'},
                'text': text,
                'entities': [{'type': 'bot_command', 'offset': 0,
                              'length': len(text)}],
            },
        })

    def test_commands(self):
        bot = bot_main.create_bot(
            '123456:TEST-TOKEN', f'{self.live_server_url}/api',
            threaded=False,
        )
        with mock.patch.object(bot, 'send_message') as send, \
                mock.patch.object(bot, 'reply_to') as reply:
            bot.process_new_updates([self.make_update('/start', 1)])
            bot.process_new_updates([self.make_update('/myinfo', 2)])

        chat_id, text = send.call_args.args
        self.assertEqual(chat_id, 555)
        self.assertTrue(text.startswith('Вы успешно зарегистрированы!'))
        self.assertIn('Имя пользователя: @irina', reply.call_args.args[1])
