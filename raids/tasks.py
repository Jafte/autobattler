from huey import crontab
from huey.contrib.djhuey import periodic_task

from gameplay.raid.standard import StandartRaid
from robots.enums import RobotStatus
from robots.models import Robot
from raids.models import Raid


@periodic_task(crontab(minute="*"))
def start_raids():
    waiting_raids: list[Robot] = list(
        Robot.objects.filter(status=RobotStatus.ON_MISSION).order_by("updated_at")[:5]
    )

    if waiting_raids:
        game = StandartRaid.create_for_users(waiting_raids)
        game.play()
        Raid.create_from_game(game)
