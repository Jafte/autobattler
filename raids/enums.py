from django.db import models


class RaidStatus(models.IntegerChoices):
    NEW = 0
    IN_PROGRESS = 1
    FINISHED = 2


class RaidRules(models.TextChoices):
    STANDARD = "Standard"
