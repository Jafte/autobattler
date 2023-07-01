from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from raids.models import RaidSession
from typing import TYPE_CHECKING
from .enums import PersonStatus

if TYPE_CHECKING:
    from persons.person import PlayerPerson


class UserPerson(models.Model):
    STATUS_DEAD = 0
    STATUS_ALIVE = 1
    STATUSES = (
        (STATUS_DEAD, 'dead'),
        (STATUS_ALIVE, 'alive'),
    )

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.SmallIntegerField(choices=PersonStatus.choices, default=PersonStatus.ALIVE)
    health = models.SmallIntegerField(default=100)
    stamina = models.SmallIntegerField(default=100)
    experience = models.BigIntegerField(default=0)

    raid_session = models.ForeignKey(
        to=RaidSession,
        on_delete=models.PROTECT,
        related_name='players',
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    died_at = models.DateTimeField(blank=True, null=True)
    epitaph = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def update_from_raid(self, person: 'PlayerPerson'):
        self.status = person.status
        self.health = person.health
        self.stamina = person.stamina
        self.experience += person.experience

        if self.status == PersonStatus.DEAD:
            self.died_at = timezone.now()
            self.epitaph = f"Убит {person.killed_by}"
