from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import NewsPost


class NewsPageTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='murka', password='test-pass-123'
        )

    def create_post(self, title, days_ago=0):
        return NewsPost.objects.create(
            title=title,
            short_description=f'Кратко: {title}',
            text=f'Первая строка {title}\nВторая строка',
            pub_date=timezone.now() - timedelta(days=days_ago),
            author=self.author,
        )

    def test_page_shows_all_fields(self):
        self.create_post('Котёнок')
        response = self.client.get(reverse('news_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Котёнок')
        self.assertContains(response, 'Кратко: Котёнок')
        self.assertContains(response, 'Первая строка Котёнок')
        self.assertContains(response, 'murka')

    def test_newest_post_first(self):
        self.create_post('Старая', days_ago=5)
        self.create_post('Свежая')
        titles = [p.title for p in self.client.get(
            reverse('news_home')).context['news']]
        self.assertEqual(titles, ['Свежая', 'Старая'])

    def test_empty_page(self):
        response = self.client.get(reverse('news_home'))
        self.assertContains(response, 'Новостей пока нет.')

    def test_deleting_author_deletes_posts(self):
        self.create_post('Котёнок')
        self.author.delete()
        self.assertEqual(NewsPost.objects.count(), 0)
