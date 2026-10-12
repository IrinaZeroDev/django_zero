from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import User


class UserModelTests(TestCase):
    def test_project_uses_users_user(self):
        self.assertEqual(settings.AUTH_USER_MODEL, 'users.User')
        self.assertIs(get_user_model(), User)

    def test_password_is_hashed(self):
        user = User.objects.create_user(
            username='murka', email='murka@example.com', password='secret-42'
        )
        self.assertNotEqual(user.password, 'secret-42')
        self.assertTrue(user.check_password('secret-42'))

    def test_email_is_unique(self):
        User.objects.create_user(username='a', email='cat@example.com')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='b', email='cat@example.com')


class UserUrlTests(SimpleTestCase):
    def test_login_and_register_pages(self):
        self.assertContains(self.client.get(reverse('login')), 'login')
        self.assertContains(self.client.get(reverse('register')), 'register')


class SettingsFromEnvTests(SimpleTestCase):
    def test_secret_key_comes_from_env_not_code(self):
        settings_code = (settings.BASE_DIR / 'mysite' / 'settings.py').read_text(
            encoding='utf-8'
        )
        self.assertTrue(settings.SECRET_KEY)
        self.assertNotIn(settings.SECRET_KEY, settings_code)
        self.assertIn("os.getenv('DJANGO_SECRET_KEY')", settings_code)
