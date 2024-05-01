from django.db import models


class RobotStatus(models.TextChoices):
    DEAD = "DEAD", "Dead"
    WAITING = "WAITING", "Waiting"
    ON_MISSION = "ON_MISSION", "On a mission"
    TRAINING = "TRAINING", "Training"


class RobotAction(models.TextChoices):
    SEND_TO_RAID = "SEND_TO_RAID", "Send to mission"
    SEND_TO_TRAINING = "SEND_TO_TRAINING", "Send to training"
    DISASSEMBLE = "DISASSEMBLE", "Disassemble"
