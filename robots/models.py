import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from typing import TYPE_CHECKING
from .enums import RobotStatus

if TYPE_CHECKING:
    from gameplay.person import PlayerPerson


class Robot(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=64, choices=RobotStatus.choices, default=RobotStatus.WAITING)
    strength = models.SmallIntegerField(default=10)
    agility = models.SmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    died_at = models.DateTimeField(blank=True, null=True)
    epitaph = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} [by {self.user}]"

    def get_absolute_url(self):
        return reverse("infra_robot_detail", args=[self.pk])

    @property
    def is_dead(self):
        return self.status == RobotStatus.DEAD

    @property
    def can_change_status(self):
        return self.status not in [RobotStatus.ON_MISSION, RobotStatus.DEAD, RobotStatus.PREPARATION]

    @property
    def tag_class(self):
        if self.status == RobotStatus.DEAD:
            return "is-danger"
        if self.status == RobotStatus.PREPARATION:
            return "is-warning"
        if self.status == RobotStatus.ON_MISSION:
            return "is-warning"
        return "12"

    def update_from_raid(self, robot_in_raid: "PlayerPerson"):
        self.status = RobotStatus.WAITING
        if robot_in_raid.is_dead:
            self.status = RobotStatus.DEAD
            self.died_at = timezone.now()
            self.epitaph = f"Убит {robot_in_raid.killed_by}"
