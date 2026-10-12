from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class BootstrapFormMixin:
    """Добавляет всем полям формы класс Bootstrap form-control."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    """Форма регистрации с почтой и необязательным телефоном."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return email


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Стандартная форма входа с оформлением Bootstrap."""
