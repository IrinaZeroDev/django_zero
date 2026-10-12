from django.db import models


class TelegramUser(models.Model):
    """Пользователь Telegram, зарегистрированный через бота."""

    user_id = models.BigIntegerField('ID в Telegram', unique=True)
    username = models.CharField(
        'Имя пользователя', max_length=255, blank=True, default=''
    )
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return f'{self.username or "без имени"} ({self.user_id})'
