from django.contrib import admin
from .models import RaidRules, RaidSession


@admin.register(RaidRules)
class AdminRaidRules(admin.ModelAdmin):
    list_display = ('title', 'max_players', 'max_bots', 'max_cycles')


@admin.register(RaidSession)
class AdminRaidSession(admin.ModelAdmin):
    list_display = ('rules', 'status', 'players')

    def players(self, obj: RaidSession):
        return obj.players.all().count()