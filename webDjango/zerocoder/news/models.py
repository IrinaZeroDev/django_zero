from django.conf import settings
from django.db import models


class NewsPost(models.Model):
    """Новость, которую публикует зарегистрированный пользователь сайта."""

    title = models.CharField('Название новости', max_length=50)
    short_description = models.CharField(
        'Краткое описание новости', max_length=200
    )
    text = models.TextField('Новость')
    pub_date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='news_posts',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
