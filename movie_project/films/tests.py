from django.test import TestCase
from django.urls import reverse

from .models import Film


class FilmPagesTests(TestCase):
    valid_data = {
        'title': 'Москва слезам не верит',
        'description': 'История трёх подруг.\nВторая строка.',
        'review': 'Смотрю каждый год.',
    }

    def test_add_page_shows_form(self):
        response = self.client.get(reverse('films:add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')
        for name in ('title', 'description', 'review'):
            self.assertContains(response, f'name="{name}"')

    def test_valid_post_saves_and_redirects(self):
        response = self.client.post(reverse('films:add'), self.valid_data)
        self.assertRedirects(response, reverse('films:list'))
        film = Film.objects.get()
        self.assertEqual(film.title, self.valid_data['title'])

    def test_list_shows_all_fields(self):
        self.client.post(reverse('films:add'), self.valid_data)
        response = self.client.get(reverse('films:list'))
        self.assertContains(response, 'Москва слезам не верит')
        self.assertContains(response, 'История трёх подруг.')
        self.assertContains(response, 'Смотрю каждый год.')

    def test_empty_fields_are_rejected(self):
        response = self.client.post(reverse('films:add'), {'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Film.objects.count(), 0)
        self.assertContains(response, 'Обязательное поле.')

    def test_empty_list(self):
        response = self.client.get(reverse('films:list'))
        self.assertContains(response, 'Фильмов пока нет.')
