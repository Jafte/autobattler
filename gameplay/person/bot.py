import random
import hashlib
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
            strength=random.randint(5, 10),
            agility=random.randint(5, 10),
        )

    def add_experience(self, value: int) -> None:
        pass
