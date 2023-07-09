from django.contrib import admin
from .models import UserFactory


@admin.register(UserFactory)
class AdminUserFactory(admin.ModelAdmin):
    list_display = ('user', 'level')
