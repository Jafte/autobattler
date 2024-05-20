from django.contrib.auth import get_user_model
from django.db import models
from typing import TYPE_CHECKING

from django.urls import reverse

from gameplay.person import BotPerson, PlayerPerson
from gameplay.raid.actions import Action
from raids.enums import RaidStatus
from robots.models import Robot
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from gameplay.raid.base import BaseRaid


class Raid(models.Model):
    bots_state = models.JSONField(_("bots state"), default=list, blank=True)
    users_state = models.JSONField(_("users state"), default=list, blank=True)
    config_state = models.JSONField(_("config state"), default=dict, blank=True)
    status = models.CharField(_("status"), choices=RaidStatus.choices, max_length=50, default=RaidStatus.NEW)
    robots = models.ManyToManyField(Robot, through='UserRaid')
    log = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Raid #{self.pk}"

    @property
    def is_finished(self) -> bool:
        return self.status == RaidStatus.FINISHED

    @property
    def action_log(self) -> list[Action]:
        result = []
        for action_json in self.log:
            action_item = Action.from_json(action_json)
            result.append(action_item)
        return result

    def get_absolute_url(self):
        return reverse("infra_raid_detail", args=[self.pk])

    def restore_gameplay_from_model(self) -> "BaseRaid":
        from gameplay.raid.base import BaseRaid

        return BaseRaid.create_for_raid(self)

    def save_gameplay_to_model(self, gameplay_raid: "BaseRaid"):
        bots_state = []
        for bot_key in gameplay_raid.bots:
            bot = gameplay_raid.persons[bot_key]
            bots_state.append(bot.to_json())
        self.bots_state = bots_state

        users_state = []
        for user_key in gameplay_raid.users:
            player = gameplay_raid.persons[user_key]
            users_state.append(player.to_json())
        self.users_state = users_state

        new_log = []
        for action_item in gameplay_raid.log:
            dict_to_save = action_item.to_json()
            new_log.append(dict_to_save)
        self.log += new_log
        self.config_state = gameplay_raid.get_config_json()
        if gameplay_raid.is_ended:
            self.status = RaidStatus.FINISHED
        self.save()

        for robot_in_raid_pk in gameplay_raid.users:
            robot_in_raid = gameplay_raid.persons[robot_in_raid_pk]
            robot = Robot.objects.get(pk=robot_in_raid_pk)
            if gameplay_raid.is_ended:
                robot.update_from_raid(robot_in_raid)
                robot.save()

            bots_killed_list = []
            robots_killed_list = []
            if robot_in_raid.kills:
                for person_uuid in robot_in_raid.kills:
                    person = gameplay_raid.persons[person_uuid]
                    if isinstance(person, BotPerson):
                        bots_killed_list.append(person_uuid)
                    if isinstance(person, PlayerPerson):
                        robots_killed_list.append(person_uuid)

            try:
                user_raid = UserRaid.objects.get(raid=self, robot=robot)
            except UserRaid.DoesNotExist:
                user_raid = UserRaid(
                    raid=self,
                    user=robot.user,
                    robot=robot,
                )

            user_raid.bots_killed_value = len(bots_killed_list)
            user_raid.bots_killed_list = bots_killed_list
            user_raid.robots_killed_value = len(robots_killed_list)
            user_raid.robots_killed_list = robots_killed_list
            user_raid.experience = robot_in_raid.experience
            user_raid.is_died = robot_in_raid.is_dead
            user_raid.save()


class UserRaid(models.Model):
    raid = models.ForeignKey(to=Raid, on_delete=models.CASCADE, related_name="raid_robots")
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="raid_robots")
    robot = models.ForeignKey(to=Robot, on_delete=models.CASCADE, related_name="raid_robots")
    bots_killed_value = models.IntegerField(default=0)
    bots_killed_list = models.JSONField(default=list, blank=True)
    robots_killed_value = models.IntegerField(default=0)
    robots_killed_list = models.JSONField(default=list, blank=True)
    experience = models.IntegerField(default=0)
    is_died = models.BooleanField(default=False)
    result = models.JSONField(default=dict, blank=True)
