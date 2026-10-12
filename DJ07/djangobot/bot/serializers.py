from rest_framework import serializers

from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """Данные пользователя, которые API отдаёт в ответах."""

    class Meta:
        model = TelegramUser
        fields = ['id', 'user_id', 'username', 'created_at']


class RegisterSerializer(serializers.Serializer):
    """Проверка данных, которые бот присылает на регистрацию.

    У Telegram-пользователя может не быть username — тогда бот
    присылает null, и мы сохраняем пустую строку.
    """

    user_id = serializers.IntegerField(min_value=1)
    username = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
