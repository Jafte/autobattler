import random
import hashlib
from gameplay.person.base import BasePerson
from robots.utils import generate_random_name


class BotPerson(BasePerson):
    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"{base_repr} [БОТ]"

    def __str__(self) -> str:
        base_str = super().__repr__()
        return f"{base_str} [БОТ]"

    @classmethod
    def create(cls) -> "BasePerson":
        random_name = generate_random_name()
        return cls(
            group='bots',
            uuid=hashlib.md5(random_name.encode("utf-8")).hexdigest(),
            name=random_name,
            max_health=100,
        )

    def add_experience(self, value: int) -> None:
        pass

    def get_damage_value(self) -> int:
        return random.randint(0, 50)
