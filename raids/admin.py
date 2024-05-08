from django.contrib import admin
from .models import Raid, UserRaid


class AdminUserRaid(admin.StackedInline):
    model = UserRaid
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Raid)
class AdminRaid(admin.ModelAdmin):
    list_display = ("pk", "created_at")
    ordering = ("-created_at",)
    inlines = [
        AdminUserRaid,
    ]

