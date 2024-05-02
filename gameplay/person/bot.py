import random
import hashlib

from gameplay.dices import roll_the_dice
from gameplay.person.base import BasePerson
from robots.utils import generate_random_name


class BotPerson(BasePerson):
    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"[БОТ] {base_repr}"

    def __str__(self) -> str:
        base_str = super().__repr__()
        return f"[БОТ] {base_str}"

    @classmethod
    def create(cls) -> "BasePerson":
        random_name = generate_random_name()
        return cls(
            uuid=hashlib.md5(random_name.encode("utf-8")).hexdigest(),
            name=random_name,
            group='bots',
            strength=roll_the_dice(10) + 10,
            agility=roll_the_dice(10) + 10,
        )

    def add_experience(self, value: int) -> None:
        pass
