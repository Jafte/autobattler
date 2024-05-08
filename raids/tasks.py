import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, lock_task

from app.utils import divide_chunks
from gameplay.raid.standard import StandartRaid
from robots.enums import RobotStatus
from robots.models import Robot
from raids.models import Raid


logger = logging.getLogger('huey')

@db_periodic_task(crontab(minute="*"))
@lock_task("start_raids")
def start_raids():
    waiting_raids: list[str] = list(
        Robot.objects.filter(status=RobotStatus.PREPARATION).order_by("updated_at").values_list('pk', flat=True)
    )

    for raid_robots_ids in divide_chunks(waiting_raids, 5):
        Robot.objects.filter(pk__in=raid_robots_ids).update(status=RobotStatus.ON_MISSION)
        play_raid(raid_robots_ids)


@db_task()
def play_raid(raid_robots_ids: list['str']):
    robot_to_raid = Robot.objects.filter(pk__in=raid_robots_ids)
    try:
        game = StandartRaid.create_for_users(robot_to_raid)
        game.play()
        Raid.create_from_game(game)
    except Exception as e:
        logger.exception(e)
        robot_to_raid.update(status=RobotStatus.WAITING)
