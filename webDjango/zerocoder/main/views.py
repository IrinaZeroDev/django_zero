from django.shortcuts import render
# from django.http import HttpResponse


def index(request):
    data = {'caption': "CatDjango"}
    return render(request, 'main/index.html', data)


def blog(request):
    data = {'caption': "CatDjango"}
    return render(request, 'main/blog.html', data)


def catalog(request):
    breeds = [
        {
            'name': 'Британская короткошёрстная',
            'origin': 'Великобритания',
            'img': '/static/main/images/british.jpg',
            'description': 'Плюшевая шерсть, спокойный характер, отлично подходят для семьи.'
        },
        {
            'name': 'Мейн-кун',
            'origin': 'США',
            'img': '/static/main/images/mainecoon.jpg',
            'description': 'Крупные, ласковые и умные кошки, очень общительны.'
        },
        {
            'name': 'Сиамская',
            'origin': 'Таиланд',
            'img': '/static/main/images/siamese.jpg',
            'description': 'Стройные, активные и болтливые, любят внимание хозяев.'
        },
        # добавляйте другие породы по аналогии
    ]
    data = {
        'caption': "CatDjango",
        'breeds': breeds
    }
    return render(request, 'main/catalog.html', data)


def about(request):
    data = {'caption': "CatDjango"}
    return render(request, 'main/about.html', data)