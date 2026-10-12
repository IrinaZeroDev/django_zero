from django.http import HttpResponse


def login(request):
    """Заглушка страницы входа, как в уроке."""
    return HttpResponse('login')


def register(request):
    """Заглушка страницы регистрации, как в уроке."""
    return HttpResponse('register')
