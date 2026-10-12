from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import TelegramUser
from .serializers import RegisterSerializer, TelegramUserSerializer


@api_view(['POST'])
def register_user(request):
    """Регистрирует пользователя Telegram.

    201 — новый пользователь создан, 200 — уже был зарегистрирован,
    400 — в запросе нет user_id или он неверный.
    """
    incoming = RegisterSerializer(data=request.data)
    incoming.is_valid(raise_exception=True)
    user, created = TelegramUser.objects.get_or_create(
        user_id=incoming.validated_data['user_id'],
        defaults={
            'username': incoming.validated_data.get('username') or '',
        },
    )
    data = TelegramUserSerializer(user).data
    if created:
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(
        {'message': 'Пользователь уже зарегистрирован', 'user': data},
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
def get_user_info(request, user_id):
    """Возвращает данные пользователя или 404, если его нет."""
    try:
        user = TelegramUser.objects.get(user_id=user_id)
    except TelegramUser.DoesNotExist:
        return Response(
            {'message': 'Пользователь не найден'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(TelegramUserSerializer(user).data)
