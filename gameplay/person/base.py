import random
from typing import Optional

from gameplay.dices import roll_the_dice
from gameplay.utils import get_level_at_experience


class BasePerson:
    # Base params from model object
    uuid: str
    name: str
    # Group for friendly
    group: str
    # Ability Scores
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    intelligence: int
    charisma: int
    # Realtime params
    action_points: int
    max_action_points: int
    health: int
    max_health: int
    level: int
    experience: int
    armor_class: int
    firewall_class: int
    stunned: bool
    acted: bool
    stunned_counter: int
    looted: bool
    killed_by: Optional[str]
    kills: Optional[list[str]]
    target: Optional[str]
    position_x: int
    position_y: int
    trails: list[list[int]]

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
            level: int = None,
            armor_class: int = None,
            firewall_class: int = None,
            max_action_points: int = None,
            action_points: int = None,
            max_health: int = None,
            health: int = None,
            killed_by: str = None,
            kills: list[str] = None,
            target: str = None,
            position_x: int = 0,
            position_y: int = 0,
            trails: list = [],
            stunned: bool = False,
            acted: bool = False,
            stunned_counter: int = 0,
            looted: bool = False,
    ) -> None:
        self.group = group.upper()
        self.uuid = str(uuid)
        self.name = name
        self.experience = experience
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.charisma = charisma

        if level is None:
            level = get_level_at_experience(self.experience)
        self.level = level

        if armor_class is None:
            armor_class = BasePerson.get_base_armor_class(self.constitution)
        self.armor_class = armor_class

        if firewall_class is None:
            firewall_class = BasePerson.get_base_firewall_class(self.wisdom)
        self.firewall_class = firewall_class

        if max_action_points is None:
            max_action_points = BasePerson.get_base_action_points(self.dexterity)
        self.max_action_points = max_action_points

        if action_points is None:
            action_points = self.max_action_points
        self.action_points = action_points

        if max_health is None:
            max_health = BasePerson.get_maximum_hp(self.level, self.constitution)
        self.max_health = max_health

        if health is None:
            health = self.max_health
        self.health = health

        self.killed_by = killed_by
        if kills is None:
            kills = []
        self.kills = kills
        self.target = target
        self.position_x = position_x
        self.position_y = position_y
        self.trails = trails
        self.stunned = stunned
        self.acted = acted
        self.stunned_counter = stunned_counter
        self.looted = looted

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

    @property
    def can_move(self) -> bool:
        if self.is_dead:
            return False
        return self.action_points > 0

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

    def move(self, x: int, y: int) -> bool:
        if not self.position_x and not self.position_y:
            self.position_x = x
            self.position_y = y
            return True

        if self.can_move:
            self.action_points -= 1
            self.trails.append([self.position_x, self.position_y])
            self.position_x = x
            self.position_y = y
            return True
        return False

    def reset_action_points(self):
        self.stunned = False
        self.acted = False
        self.action_points = self.max_action_points

    def add_experience(self, value: int) -> None:
        self.experience += value

    def select_target(self, persons_list: list['BasePerson']) -> None:
        self.target = None
        possible_targets = []
        for person in persons_list:
            if person.is_dead:
                continue
            if self.uuid == person.uuid:
                continue
            if person.group == self.group:
                continue
            possible_targets.append(person.uuid)
        if possible_targets:
            self.target = random.choice(possible_targets)

    def loot(self):
        self.looted = True

    def stun(self):
        self.stunned = True
        self.stunned_counter = 1

    def ability_checks(self):
        if self.stunned:
            dice_roll = roll_the_dice(20)
            if dice_roll == 20:
                self.stunned = False
                self.stunned_counter = 0
                return
            if dice_roll == 1:
                self.stun()
                return
            if dice_roll + BasePerson.get_ability_modifier(self.wisdom) > (10 - self.stunned_counter * 2):
                self.stunned = False
                self.stunned_counter = 0

    def to_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "group": self.group,
            "experience": self.experience,
            "level": self.level,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "wisdom": self.wisdom,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "armor_class": self.armor_class,
            "firewall_class": self.firewall_class,
            "action_points": self.action_points,
            "max_action_points": self.max_action_points,
            "health": self.health,
            "max_health": self.max_health,
            "killed_by": self.killed_by,
            "kills": self.kills,
            "position_y": self.position_y,
            "position_x": self.position_x,
            "trails": self.trails,
            "stunned": self.stunned,
            "acted": self.acted,
            "target": self.target,
        }

    @classmethod
    def from_json(cls, data: dict) -> 'BasePerson':
        return cls(**data)

    def attack_check(self, person: 'BasePerson') -> bool:
        if person.armor_class > self.get_attack_rate():
            return False
        return True

    def hack_check(self, person: 'BasePerson') -> bool:
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
    def get_base_action_points(dexterity: int) -> int:
        action_points = 1 + BasePerson.get_ability_modifier(dexterity) // 2
        return max(action_points, 1)
