from persons.enums import PersonStatus


class GameplayPersonBase:
    uuid: str
    name: str
    status: 'PersonStatus'
    health: int
    inventory: dict
    experience: int
    killed_by: str

    def __init__(self, name: str, uuid: str, health: int, inventory: dict) -> None:
        self.name = name
        self.uuid = uuid
        self.health = health
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
