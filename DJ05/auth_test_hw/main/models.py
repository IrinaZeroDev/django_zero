from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message='Введите номер из 10–15 цифр, можно с «+» в начале.',
)


class CustomUser(AbstractUser):
    """Пользователь с уникальной почтой и необязательным телефоном."""

    email = models.EmailField('Электронная почта', unique=True)
    phone_number = models.CharField(
        'Номер телефона',
        max_length=16,
        blank=True,
        validators=[phone_validator],
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
