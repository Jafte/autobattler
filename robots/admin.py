from django.contrib import admin

from raids.admin import AdminUserRaid
from .models import Robot


@admin.register(Robot)
class AdminRobot(admin.ModelAdmin):
    list_display = ("name", "status", "created_at", "user",)
    list_filter = ("status",)
    inlines = [
        AdminUserRaid
    ]

