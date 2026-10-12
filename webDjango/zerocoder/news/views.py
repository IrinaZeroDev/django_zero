from django.shortcuts import render

from .models import NewsPost


def home(request):
    """Отображает страницу со всеми новостями, свежие — сверху."""
    news = NewsPost.objects.select_related('author')
    context = {
        'caption': 'CatDjango',
        'news': news,
    }
    return render(request, 'news/news.html', context)
