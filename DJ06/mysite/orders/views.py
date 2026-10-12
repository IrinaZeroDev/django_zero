from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def user_orders(request, user_id):
    """Список заказов пользователя.

    Модель пользователя берём через get_user_model(), а не импортом
    из приложения users.
    """
    user = get_object_or_404(get_user_model(), pk=user_id)
    lines = [str(order) for order in user.orders.all()]
    body = '\n'.join(lines) or 'Заказов нет'
    return HttpResponse(
        f'Заказы {user.username}:\n{body}',
        content_type='text/plain; charset=utf-8',
    )
