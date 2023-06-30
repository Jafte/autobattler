from django.db import models


class PersonStatus(models.IntegerChoices):
    ALIVE = 1
    DEAD = 0
