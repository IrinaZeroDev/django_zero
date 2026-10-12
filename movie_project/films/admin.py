from django.contrib import admin

from .models import Film


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description', 'review')
