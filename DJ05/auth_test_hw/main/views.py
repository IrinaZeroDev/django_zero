from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomUserCreationForm


class IndexView(TemplateView):
    """Главная страница, доступна всем."""

    template_name = 'main/index.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    """Профиль: гостя перенаправляет на страницу входа (LOGIN_URL)."""

    template_name = 'main/profile.html'


class RegisterView(CreateView):
    """Регистрация; после успеха — переход на страницу входа."""

    form_class = CustomUserCreationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')
