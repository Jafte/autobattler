from django.db import models
from django.contrib.auth import get_user_model
from persons.models import UserPerson
from persons.enums import PersonStatus


class UserFactory(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    level = models.SmallIntegerField(default=1)
    active_user_person_limit = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user} lvl {self.level}"

    @property
    def can_create_robots(self) -> bool:
        if getattr(self, "_active_user_person_count", None) is None:
            self._active_user_person_count = UserPerson.objects.filter(user=self.user, status=PersonStatus.ALIVE).count()
        return self._active_user_person_count < self.active_user_person_limit
