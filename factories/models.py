from django.db import models
from django.contrib.auth import get_user_model


class UserFactory(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    level = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user} lvl {self.level}"
