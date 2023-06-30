import random
import hashlib
from .enums import PersonStatus
from .utils import generate_random_name

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import UserPerson


class Person:
    uuid: str
    name: str
    status: 'PersonStatus'
    health: int
    stamina: int
    inventory: dict
    experience: int
    killed_by: str

    def __init__(self, name: str, uuid: str, health: int, stamina: int, inventory: dict) -> None:
        self.name = name
        self.uuid = uuid
        self.health = health
        self.stamina = stamina
        self.inventory = inventory
        self.status = PersonStatus.ALIVE
        self.experience = 0
        self.killed_by = ''

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"

    def is_alive(self) -> bool:
        return self.status == PersonStatus.ALIVE

    def hit(self, value: int) -> None:
        self.health -= value
        if self.health <= 0:
            self.status = PersonStatus.DEAD

    def heal(self, value: int) -> None:
        if not self.is_alive():
            return
        if self.health < 100:
            self.health += value
        if self.health > 100:
            self.health = 100

    def add_experience(self, value: int) -> None:
        raise NotImplementedError()

    def get_damage_value(self) -> int:
        raise NotImplementedError()


class BotPerson(Person):
    def __repr__(self) -> str:
        return f"{self.name} [бот]"

    @classmethod
    def create(cls) -> 'Person':
        random_name = generate_random_name()
        return cls(
            name=random_name,
            uuid=hashlib.md5(random_name.encode('utf-8')).hexdigest(),
            health=100,
            stamina=100,
            inventory={},
        )

    def add_experience(self, value: int) -> None:
        pass

    def get_damage_value(self) -> int:
        return random.randint(0, 50)


class PlayerPerson(Person):
    @classmethod
    def create(cls, model: UserPerson) -> 'Person':
        return cls(
            name=model.name,
            uuid=str(model.pk),
            health=model.health,
            stamina=model.stamina,
            inventory={},
        )

    def add_experience(self, value: int) -> None:
        self.experience += value

    def get_damage_value(self) -> int:
        return random.randint(0, 100)
