from django.contrib import admin
from accounts.models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("pk",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
