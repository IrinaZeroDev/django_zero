from django.shortcuts import redirect, render

from .forms import FilmForm
from .models import Film


def film_list(request):
    """Отображает все сохранённые фильмы, новые — сверху."""
    context = {'films': Film.objects.all()}
    return render(request, 'films/film_list.html', context)


def add_film(request):
    """Показывает форму и сохраняет новый фильм в базу данных."""
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('films:list')
    else:
        form = FilmForm()
    context = {'form': form}
    return render(request, 'films/add_film.html', context)
