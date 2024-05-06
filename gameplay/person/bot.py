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
    def create(cls, max_level: int = 0) -> "BasePerson":
        random_name = generate_random_name()
        if roll_the_dice(20) == 20:
            strength = 20
            dexterity = 20
            constitution = 20
            wisdom = 20
            intelligence = 20
            charisma = 20
            level = 20 if not max_level else max_level
        else:
            strength = 6 + roll_the_dice(6) + roll_the_dice(6)
            dexterity = 6 + roll_the_dice(6) + roll_the_dice(6)
            constitution = 6 + roll_the_dice(6) + roll_the_dice(6)
            wisdom = 6 + roll_the_dice(6) + roll_the_dice(6)
            intelligence = 6 + roll_the_dice(6) + roll_the_dice(6)
            charisma = 6 + roll_the_dice(6) + roll_the_dice(6)
            level = roll_the_dice(max_level) if max_level > 1 else max_level

        return cls(
            uuid=hashlib.md5(random_name.encode("utf-8")).hexdigest(),
            name=random_name,
            group='bots',
            experience=BasePerson.LEVEL_PROGRESSION[level],
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            wisdom=wisdom,
            intelligence=intelligence,
            charisma=charisma,
        )

    def add_experience(self, value: int) -> None:
        pass
