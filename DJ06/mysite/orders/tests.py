from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order


class OrderTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='murka', email='murka@example.com', password='x'
        )
        Order.objects.create(user=self.user, product='Корм', price=500)
        Order.objects.create(user=self.user, product='Лежанка', price=1500)

    def test_user_has_orders_via_related_name(self):
        products = sorted(o.product for o in self.user.orders.all())
        self.assertEqual(products, ['Корм', 'Лежанка'])

    def test_deleting_user_deletes_orders(self):
        self.user.delete()
        self.assertFalse(Order.objects.exists())

    def test_user_orders_page(self):
        response = self.client.get(
            reverse('user_orders', args=[self.user.pk])
        )
        self.assertContains(response, 'Заказы murka')
        self.assertContains(response, 'Корм — 500 ₽')

    def test_unknown_user_gives_404(self):
        response = self.client.get(reverse('user_orders', args=[999]))
        self.assertEqual(response.status_code, 404)
