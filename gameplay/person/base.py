import random
from typing import Optional

from gameplay.dices import roll_the_dice


class BasePerson:
    uuid: str
    group: str
    name: str
    strength: int
    agility: int
    health: int
    experience: int
    killed_by: Optional["BasePerson"]
    kills: Optional[list["BasePerson"]]
    action_log: list[str]

    def __init__(self, uuid: str, name: str, group: str, strength: int, agility: int) -> None:
        self.group = group.upper()
        self.uuid = uuid
        self.name = name
        self.strength = strength
        self.agility = agility
        self.health = self.max_health
        self.experience = 0
        self.killed_by = None
        self.kills = []
        self.action_log = []

    def __str__(self) -> str:
        return f"{self.name} [{self.health}/{self.max_health}]"

    def __repr__(self) -> str:
        return f"{self.name} [{self.health}/{self.max_health}]"

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    @property
    def need_healing(self) -> bool:
        return self.health < self.max_health

    @property
    def max_health(self) -> int:
        return 10 + self.strength * 10

    def get_initiative(self) -> int:
        return roll_the_dice(20) + self.agility

    def get_defence_rate(self) -> int:
        return roll_the_dice(20) + self.agility

    def get_attack_rate(self) -> int:
        return roll_the_dice(20) + self.agility

    def get_damage_volume(self) -> int:
        return roll_the_dice(10) + self.strength

    def get_healing_volume(self) -> int:
        return roll_the_dice(10) + self.strength

    def hit(self, value: int):
        if self.is_dead:
            return
        self.health -= value
        if self.health < 0:
            self.health = 0

    def heal(self, value: int) -> None:
        if self.is_dead:
            return
        if self.health == self.max_health:
            return
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health

    def add_experience(self, value: int) -> None:
        self.experience += value

    def log(self, message: str):
        self.action_log.append(message)

    def attack(self, person: 'BasePerson') -> bool:
        if person.get_defence_rate() > self.get_attack_rate():
            return False
        return True
