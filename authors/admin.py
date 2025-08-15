from django.contrib import admin
from authors.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'id', 'author',
    list_display_links = 'id', 'author',