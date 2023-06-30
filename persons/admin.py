from django.contrib import admin
from .models import UserPerson


@admin.register(UserPerson)
class AdminUserPerson(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'created_at')
    raw_id_fields = ("raid_session",)
