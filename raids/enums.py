from django.db import models


class RaidStatus(models.TextChoices):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"


class RaidRules(models.TextChoices):
    STANDARD = "Standard"
