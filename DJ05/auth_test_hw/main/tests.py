from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser

PASSWORD = 'Sl0zhnyi-parol-42'


class RegistrationTests(TestCase):
    def register(self, **overrides):
        data = {
            'username': 'murka',
            'email': 'murka@example.com',
            'phone_number': '+79991234567',
            'password1': PASSWORD,
            'password2': PASSWORD,
        }
        data.update(overrides)
        return self.client.post(reverse('register'), data)

    def test_project_uses_custom_user(self):
        self.assertIs(get_user_model(), CustomUser)

    def test_register_saves_fields_and_redirects_to_login(self):
        response = self.register()
        self.assertRedirects(response, reverse('login'))
        user = CustomUser.objects.get(username='murka')
        self.assertEqual(user.email, 'murka@example.com')
        self.assertEqual(user.phone_number, '+79991234567')
        self.assertTrue(user.check_password(PASSWORD))

    def test_phone_is_optional_for_several_users(self):
        self.register(phone_number='')
        self.register(username='barsik', email='barsik@example.com',
                      phone_number='')
        self.assertEqual(CustomUser.objects.filter(phone_number='').count(), 2)

    def test_email_is_required(self):
        response = self.register(email='')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())

    def test_duplicate_email_rejected_ignoring_case(self):
        self.register()
        response = self.register(username='barsik', email='MURKA@example.com')
        self.assertContains(response, 'уже зарегистрирован')
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_invalid_phone_rejected(self):
        response = self.register(phone_number='12-ab')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())

    def test_password_not_echoed_back_on_error(self):
        response = self.register(email='')
        self.assertNotContains(response, PASSWORD)


class AccessTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='murka', email='murka@example.com', password=PASSWORD
        )

    def test_profile_redirects_guest_to_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('profile')}"
        )

    def test_login_redirects_to_profile_with_user_data(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'murka', 'password': PASSWORD},
            follow=True,
        )
        self.assertRedirects(response, reverse('profile'))
        self.assertContains(response, 'murka@example.com')
        self.assertContains(response, 'не указан')

    def test_wrong_password_shows_error(self):
        response = self.client.post(
            reverse('login'), {'username': 'murka', 'password': 'wrong'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alert-danger')

    def test_logout_by_post_redirects_to_index(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        guest = self.client.get(reverse('profile'))
        self.assertEqual(guest.status_code, 302)

    def test_logout_by_get_is_not_allowed(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)

    def test_navigation_links(self):
        guest_page = self.client.get(reverse('index'))
        for name in ('index', 'profile', 'login', 'register'):
            self.assertContains(guest_page, f'href="{reverse(name)}"')
        self.client.force_login(self.user)
        user_page = self.client.get(reverse('index'))
        self.assertContains(user_page, f'action="{reverse("logout")}"')
        self.assertContains(user_page, 'csrfmiddlewaretoken')
