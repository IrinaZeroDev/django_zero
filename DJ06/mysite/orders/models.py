from django.conf import settings
from django.db import models


class Order(models.Model):
    """Заказ пользователя.

    Модель пользователя указана строкой из настроек, а не импортом
    из users.models, — так orders не зависит от users напрямую и
    циклического импорта не возникает.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь',
    )
    product = models.CharField('Товар', max_length=100)
    price = models.PositiveIntegerField('Цена, ₽')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.product} — {self.price} ₽'
