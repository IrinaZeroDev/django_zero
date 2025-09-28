from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog', views.catalog, name='page2'),
    path('blog', views.blog, name='page3'),
    path('about', views.about, name='page4')
]