from django.db import models


class RobotStatus(models.TextChoices):
    DEAD = "DEAD", "Нет сигнала"
    WAITING = "WAITING", "В режиме ожидании"
    ON_MISSION = "ON_MISSION", "Исполняет задание"


class RobotAction(models.TextChoices):
    SEND_TO_RAID = "SEND_TO_RAID", "Отправить на миссию"
    DISASSEMBLE = "DISASSEMBLE", "Разобрать"
