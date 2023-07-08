from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from raids.models import UserRaid
from typing import TYPE_CHECKING
from .enums import PersonStatus

if TYPE_CHECKING:
    from gameplay.person import GameplayPersonPlayer


class UserPerson(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.SmallIntegerField(choices=PersonStatus.choices, default=PersonStatus.ALIVE)
    health = models.SmallIntegerField(default=100)
    experience = models.BigIntegerField(default=0)

    raid_session = models.ForeignKey(
        to=UserRaid,
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

    def update_from_raid(self, gameplay_person: 'GameplayPersonPlayer'):
        self.status = gameplay_person.status
        self.health = gameplay_person.health
        self.experience += gameplay_person.experience

        if self.status == PersonStatus.DEAD:
            self.died_at = timezone.now()
            self.epitaph = f"Убит {gameplay_person.killed_by}"
