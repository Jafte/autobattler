import random
from typing import Optional

from gameplay.dices import roll_the_dice


class BasePerson:
    # Base params from model object
    uuid: str
    name: str
    # Group for friendly
    group: str
    # Ability Scores
    speed: int
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    intelligence: int
    charisma: int
    # Realtime params
    health: int
    max_health: int
    level: int
    experience: int
    armor_class: int
    firewall_class: int
    stunned: bool
    killed_by: Optional["BasePerson"]
    kills: Optional[list["BasePerson"]]
    action_log: list[str]
    target: Optional["BasePerson"]
    position_x: int
    position_y: int

    LEVEL_PROGRESSION = [
        0,
        0,
        300,
        900,
        2700,
        6500,  # 5
        14000,
        23000,
        34000,
        48000,
        64000,  # 10
        85000,
        100000,
        120000,
        140000,
        165000,  # 15
        195000,
        225000,
        265000,
        305000,
        355000,  # 20
    ]

    def __init__(
            self,
            uuid: str,
            name: str,
            group: str,
            experience: int,
            strength: int,
            dexterity: int,
            constitution: int,
            wisdom: int,
            intelligence: int,
            charisma: int,
    ) -> None:
        self.group = group.upper()
        self.uuid = uuid
        self.name = name
        self.experience = experience
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.charisma = charisma

        self.level = BasePerson.get_level_at_experience(self.experience)
        self.armor_class = BasePerson.get_base_armor_class(self.constitution)
        self.firewall_class = BasePerson.get_base_firewall_class(self.wisdom)
        self.speed = BasePerson.get_base_speed(self.dexterity)
        self.health = self.max_health = BasePerson.get_maximum_hp(self.level, self.constitution)

        self.killed_by = None
        self.kills = []
        self.action_log = []
        self.target = None
        self.position_x = 0
        self.position_y = 0
        self.stunned = False

    def __str__(self) -> str:
        return f"{self.name} [{self.level}] [{self.health}/{self.max_health}]"

    def __repr__(self) -> str:
        return f"{self.name} [{self.level}] [{self.health}/{self.max_health}]"

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    @property
    def need_healing(self) -> bool:
        return self.is_alive and self.health < self.max_health

    def get_initiative(self) -> int:
        value = roll_the_dice(20) + BasePerson.get_ability_modifier(self.intelligence)
        return max(value, 0)

    def get_hack_rate(self) -> int:
        dice_roll = roll_the_dice(20)
        if dice_roll == 20:
            return 1000
        if dice_roll == 1:
            return 0
        value = dice_roll + BasePerson.get_ability_modifier(self.charisma)
        return max(value, 0)

    def get_attack_rate(self) -> int:
        dice_roll = roll_the_dice(20)
        if dice_roll == 20:
            return 1000
        if dice_roll == 1:
            return 0
        value = dice_roll + BasePerson.get_ability_modifier(self.intelligence)
        return max(value, 0)

    def get_damage_volume(self) -> int:
        value = roll_the_dice(6) + BasePerson.get_ability_modifier(self.strength)
        return max(value, 0)

    def get_healing_volume(self) -> int:
        value = roll_the_dice(6) + BasePerson.get_ability_modifier(self.constitution)
        return max(value, 0)

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

    def json(self):
        return {
            "name": self.name,
            "level": self.level,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "wisdom": self.wisdom,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "killed_by": str(self.killed_by.uuid) if self.killed_by else '',
            "kills": [str(x.uuid) for x in self.kills],
        }

    def attack(self, person: 'BasePerson') -> bool:
        if person.armor_class > self.get_attack_rate():
            return False
        return True

    def hack(self, person: 'BasePerson') -> bool:
        if person.firewall_class > self.get_hack_rate():
            return False
        return True

    @staticmethod
    def get_ability_modifier(number: int) -> int:
        return (number - 10) // 2

    @staticmethod
    def get_maximum_hp(level: int, constitution: int) -> int:
        return (
                10
                + 6 * (level - 1)
                + BasePerson.get_ability_modifier(constitution)
        )

    @staticmethod
    def get_base_armor_class(constitution: int) -> int:
        return 10 + BasePerson.get_ability_modifier(constitution)

    @staticmethod
    def get_base_firewall_class(wisdom: int) -> int:
        return 15 + BasePerson.get_ability_modifier(wisdom)

    @staticmethod
    def get_base_speed(dexterity: int) -> int:
        speed = 1 + BasePerson.get_ability_modifier(dexterity) // 2
        return max(speed, 1)

    @staticmethod
    def get_level_at_experience(experience: int) -> int:
        for level, threshold in enumerate(BasePerson.LEVEL_PROGRESSION):
            if experience >= threshold:
                continue
            return level - 1
        return 20

    def select_target(self, persons_list: list['BasePerson']) -> None:
        self.target = None
        for person in persons_list:
            if person.is_dead:
                continue
            if self.uuid == person.uuid:
                continue
            if person.group == self.group:
                continue
            self.target = person
            break
