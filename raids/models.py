from django.contrib.auth import get_user_model
from django.db import models
from typing import TYPE_CHECKING

from gameplay.person import BotPerson, PlayerPerson
from robots.models import Robot
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from gameplay.raid.standard import StandartRaid


class Raid(models.Model):
    bots_result = models.JSONField(_("bots result"), default=dict, blank=True)
    users_result = models.JSONField(_("users result"), default=dict, blank=True)
    robots = models.ManyToManyField(Robot, through='UserRaid')
    action_log = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Raid #{self.pk}"

    @classmethod
    def create_from_game(cls, gameplay_raid: "StandartRaid"):
        raid = cls()
        bot_dict_to_save = {}
        for bot_key in gameplay_raid.bots:
            bot = gameplay_raid.persons[bot_key]
            bot_dict_to_save[str(bot.uuid)] = {
                "name": bot.name,
                "health": bot.health,
                "killed_by": bot.killed_by.name if bot.killed_by else '',
                "kills": list(map(lambda x: x.name, bot.kills)),
            }
        raid.bots_result = bot_dict_to_save

        users_dict_to_save = {}
        for user_key in gameplay_raid.users:
            player = gameplay_raid.persons[user_key]
            users_dict_to_save[str(player.uuid)] = {
                "name": player.name,
                "health": player.health,
                "killed_by": player.killed_by.name if player.killed_by else '',
                "experience": player.experience,
                "kills": list(map(lambda x: x.name, player.kills)),
            }
        raid.users_result = users_dict_to_save

        raid.action_log = gameplay_raid.action_log
        raid.save()

        for robot_in_raid_pk in gameplay_raid.users:
            robot_in_raid = gameplay_raid.persons[robot_in_raid_pk]
            robot = Robot.objects.get(pk=robot_in_raid_pk)
            robot.update_from_raid(robot_in_raid)
            robot.save()
            bots_killed_list = list(filter(lambda x: isinstance(x, BotPerson), robot_in_raid.kills))
            robots_killed_list = list(filter(lambda x: isinstance(x, PlayerPerson), robot_in_raid.kills))
            user_raid = UserRaid(
                raid=raid,
                user=robot.user,
                robot=robot,
                bots_killed_value=len(bots_killed_list),
                bots_killed_list=list(map(lambda x: x.name, bots_killed_list)),
                robots_killed_value=len(robots_killed_list),
                robots_killed_list=list(map(lambda x: x.name, robots_killed_list)),
                experience=robot_in_raid.experience,
                is_died=robot_in_raid.is_dead,
                result={
                    "health": robot_in_raid.health,
                    "killed_by": robot_in_raid.killed_by.name if robot_in_raid.killed_by else '',
                    "log": robot_in_raid.action_log,
                }
            )
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
