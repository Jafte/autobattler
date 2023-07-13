from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task

from gameplay.raid.standard import GameplayRaid
from raids.enums import RaidStatus
from raids.models import UserRaid


@periodic_task(crontab(minute='*'))
def start_raids():
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    new_raids = UserRaid.objects.filter(status=RaidStatus.NEW, created_at__lte=five_minutes_ago)

    for raid in new_raids:
        if raid.players.count() == 0:
            continue

        raid.status = RaidStatus.IN_PROGRESS
        raid.save()

        game = GameplayRaid.create_from_user_raid(raid)
        game.start()
        game.play()

        raid.update_from_raid(game)
