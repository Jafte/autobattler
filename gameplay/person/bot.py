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
        if roll_the_dice(20) == 20:
            strength = 20
            agility = 20
        else:
            strength = 5 + roll_the_dice(6) + roll_the_dice(6)
            agility = 5 + roll_the_dice(6) + roll_the_dice(6)

        return cls(
            uuid=hashlib.md5(random_name.encode("utf-8")).hexdigest(),
            name=random_name,
            group='bots',
            strength=strength,
            agility=agility,
        )

    def add_experience(self, value: int) -> None:
        pass
