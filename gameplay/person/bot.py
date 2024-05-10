import random
import hashlib

from gameplay.dices import roll_the_dice, roll_ability_dice
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
        strength = roll_ability_dice()
        dexterity = roll_ability_dice()
        constitution = roll_ability_dice()
        wisdom = roll_ability_dice()
        intelligence = roll_ability_dice()
        charisma = roll_ability_dice()
        level = roll_the_dice(max_level) if max_level > 1 else max_level

        bot = cls(
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
        if roll_the_dice(20) == 20:
            max_value = 20 + max_level // 2
            ability = random.choice([
                "strength",
                "dexterity",
                "constitution",
                "wisdom",
                "intelligence",
                "charisma",
            ])
            setattr(bot, ability, max_value)

        return bot

    def add_experience(self, value: int) -> None:
        pass
