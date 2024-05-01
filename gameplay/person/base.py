from typing import Optional


class BasePerson:
    uuid: str
    group: str
    name: str
    health: int
    max_health: int
    experience: int
    killed_by: Optional["BasePerson"]
    kills: Optional[list["BasePerson"]]

    def __init__(self, group: str, uuid: str, name: str, max_health: int) -> None:
        self.group = group.upper()
        self.uuid = uuid
        self.name = name
        self.health = self.max_health = max_health
        self.experience = 0
        self.killed_by = None
        self.kills = []

    def __str__(self) -> str:
        return f"{self.name} [{self.health}/{self.max_health}]"

    def __repr__(self) -> str:
        return f"{self.name} [{self.health}/{self.max_health}]"

    def is_alive(self) -> bool:
        return self.health > 0

    def is_dead(self) -> bool:
        return self.health <= 0

    def hit(self, value: int) -> None:
        if self.is_dead():
            return
        self.health -= value
        if self.health < 0:
            self.health = 0

    def heal(self, value: int) -> None:
        if self.is_dead():
            return
        if self.health == self.max_health:
            return
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health

    def add_experience(self, value: int) -> None:
        raise NotImplementedError()

    def get_damage_value(self) -> int:
        raise NotImplementedError()
