from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь сайта: имя, фамилия, пароль и логин — из AbstractUser."""

    email = models.EmailField('Электронная почта', max_length=255, unique=True)
    address = models.TextField('Адрес', blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
