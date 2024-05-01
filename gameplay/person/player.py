import random
from gameplay.person.base import BasePerson

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from robots.models import Robot


class PlayerPerson(BasePerson):
    @classmethod
    def create(cls, model: "Robot") -> "BasePerson":
        return cls(
            group=f"user_{model.user.pk}",
            uuid=model.uuid,
            name=model.name,
            max_health=model.max_health,
        )

    def add_experience(self, value: int) -> None:
        self.experience += value

    def get_damage_value(self) -> int:
        return random.randint(0, 100)
