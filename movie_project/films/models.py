from django.db import models


class Film(models.Model):
    """Фильм с описанием и отзывом зрителя."""

    title = models.CharField('Название фильма', max_length=200)
    description = models.TextField('Описание фильма')
    review = models.TextField('Отзыв')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
