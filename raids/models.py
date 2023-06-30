from django.db import models
from .enums import RaidStatus


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
    status = models.SmallIntegerField(choices=RaidStatus.choices, default=RaidStatus.NEW)
    action_log = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.rules} #{self.pk}"
