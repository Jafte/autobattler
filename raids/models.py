from django.db import models
from django.utils import timezone
from typing import TYPE_CHECKING
from .enums import RaidStatus

if TYPE_CHECKING:
    from gameplay.raid.standard import GameplayRaid


class UserRaid(models.Model):
    rules = models.JSONField(default=dict)
    bots = models.JSONField(default=dict, blank=True)
    users = models.JSONField(default=dict, blank=True)
    status = models.SmallIntegerField(choices=RaidStatus.choices, default=RaidStatus.NEW)
    action_log = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.rules} #{self.pk}"

    def update_from_raid(self, gameplay_raid: 'GameplayRaid'):
        from persons.models import UserPerson

        self.status = gameplay_raid.status
        bot_dict_to_save = {}
        for bot in gameplay_raid.bots.values():
            bot_dict_to_save[bot.uuid] = {
                'name': bot.name,
                'status': bot.status,
                'health': bot.health,
                'killed_by': bot.killed_by
            }
        self.bots = bot_dict_to_save
        self.action_log = gameplay_raid.action_log
        self.finished_at = timezone.now()

        users_dict_to_save = {}
        for person in gameplay_raid.players.values():
            users_dict_to_save[person.uuid] = {
                'name': person.name,
                'status': person.status,
                'health': person.health,
                'killed_by': person.killed_by,
                'experience': person.experience,
            }
            model = UserPerson.objects.get(pk=person.uuid)
            model.update_from_raid(person)
            model.raid_session = None
            model.save()

        self.users = users_dict_to_save

        self.save()
