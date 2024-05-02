import random
from gameplay.person.base import BasePerson

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from robots.models import Robot


class PlayerPerson(BasePerson):
    @classmethod
    def create(cls, robot_model: "Robot") -> "BasePerson":
        return cls(
            uuid=robot_model.uuid,
            name=robot_model.name,
            group=f"user_{robot_model.user.pk}",
            strength=robot_model.strength,
            agility=robot_model.agility,
        )
