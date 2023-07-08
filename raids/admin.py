from django.contrib import admin
from .models import UserRaid


@admin.register(UserRaid)
class AdminRaidSession(admin.ModelAdmin):
    list_display = ('rules', 'status', 'players')

    def players(self, obj: UserRaid):
        return obj.players.all().count()
