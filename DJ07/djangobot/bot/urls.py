from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('user/<int:user_id>/', views.get_user_info, name='user_info'),
]
