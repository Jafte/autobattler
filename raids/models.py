import json
from django.db import models
from django.utils import timezone
from typing import TYPE_CHECKING
from .enums import RaidStatus

if TYPE_CHECKING:
    from raids.raid import Raid as Game


class RaidRules(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    max_players = models.SmallIntegerField()
    max_bots = models.SmallIntegerField()
    max_cycles = models.SmallIntegerField()

    def __str__(self):
        return self.title


class RaidSession(models.Model):
    rules = models.ForeignKey(to=RaidRules, on_delete=models.PROTECT)
    bots = models.JSONField(default=dict, blank=True)
    users = models.JSONField(default=dict, blank=True)
    status = models.SmallIntegerField(choices=RaidStatus.choices, default=RaidStatus.NEW)
    action_log = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.rules} #{self.pk}"

    def update_from_raid(self, game: 'Game'):
        from persons.models import UserPerson

        self.status = game.status
        bot_dict_to_save = {}
        for bot in game.bots.values():
            bot_dict_to_save[bot.uuid] = {
                'name': bot.name,
                'status': bot.status,
                'health': bot.health,
                'stamina': bot.stamina,
                'killed_by': bot.killed_by
            }
        self.bots = bot_dict_to_save
        self.action_log = game.action_log
        self.finished_at = timezone.now()

        users_dict_to_save = {}
        for person in game.players.values():
            users_dict_to_save[person.uuid] = {
                'name': person.name,
                'status': person.status,
                'health': person.health,
                'stamina': person.stamina,
                'killed_by': person.killed_by,
                'experience': person.experience,
            }
            model = UserPerson.objects.get(pk=person.uuid)
            model.update_from_raid(person)
            model.raid_session = None
            model.save()

        self.users = users_dict_to_save

        self.save()
