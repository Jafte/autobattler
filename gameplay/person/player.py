import random
from gameplay.person.base import GameplayPersonBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from persons.models import UserPerson


class GameplayPersonPlayer(GameplayPersonBase):
    @classmethod
    def create(cls, model: 'UserPerson') -> 'GameplayPersonBase':
        return cls(
            name=model.name,
            uuid=str(model.pk),
            health=model.health,
            inventory={},
        )

    def add_experience(self, value: int) -> None:
        self.experience += value

    def get_damage_value(self) -> int:
        return random.randint(0, 100)
