import random
import hashlib
from gameplay.person.base import GameplayPersonBase
from persons.utils import generate_random_name


class GameplayPersonBot(GameplayPersonBase):
    def __repr__(self) -> str:
        return f"{self.name} [бот]"

    @classmethod
    def create(cls) -> 'GameplayPersonBase':
        random_name = generate_random_name()
        return cls(
            name=random_name,
            uuid=hashlib.md5(random_name.encode('utf-8')).hexdigest(),
            health=100,
            inventory={},
        )

    def add_experience(self, value: int) -> None:
        pass

    def get_damage_value(self) -> int:
        return random.randint(0, 50)
