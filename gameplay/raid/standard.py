import random

from app.utils import plural
from gameplay.dices import roll_the_dice
from gameplay.person import BasePerson, BotPerson, PlayerPerson
from typing import Dict, List, Union
from robots.models import Robot


class StandartRaid:
    persons: Dict[str, BasePerson]
    users: List[str]
    bots: List[str]
    looted_bodies: List[str]
    action_log: List[str]
    max_x: int
    max_y: int
    max_rounds: int
    __map: dict[str, list[BasePerson]]

    def __init__(self, max_x: int, max_y: int, max_rounds: int) -> None:
        self.persons = {}
        self.users = []
        self.bots = []
        self.max_x = max_x
        self.max_y = max_y
        self.max_rounds = max_rounds
        self.action_log = []
        self.looted_bodies = []

        self.__map = {}

    @classmethod
    def create_for_user(cls, robot: "Robot") -> "StandartRaid":
        raid = cls(
            max_x=20,
            max_y=20,
            max_rounds=50,
        )
        person = PlayerPerson.create(robot)
        raid.join(person)

        for _ in range(roll_the_dice(20)):
            bot = BotPerson.create(max_level=person.level)
            raid.join(bot)

        return raid

    def __str__(self) -> str:
        return f"Raid"

    def __repr__(self) -> str:
        return f"Raid"

    def join(self, person: BasePerson) -> None:
        self.move_person(
            person=person,
            x=random.randint(1, self.max_x),
            y=random.randint(1, self.max_y)
        )

        self.persons[person.uuid] = person
        if isinstance(person, PlayerPerson):
            if person.uuid not in self.users:
                self.users.append(person.uuid)
        if isinstance(person, BotPerson):
            if person.uuid not in self.bots:
                self.bots.append(person.uuid)

    def play(self) -> None:
        for _ in range(self.max_rounds):
            self._check_action()
            for person in self.persons.values():
                for __ in range(person.speed):
                    new_x_min = max(person.position_x - 1, 1)
                    new_x_max = min(person.position_x + 1, self.max_x)
                    new_y_min = max(person.position_y - 1, 1)
                    new_y_max = min(person.position_y + 1, self.max_y)
                    self.move_person(
                        person=person,
                        x=random.choice([new_x_min, new_x_max]),
                        y=random.choice([new_y_min, new_y_max]),
                    )
                    self._check_action()

            all_dead = True

            for user_key in self.users:
                person = self.persons[user_key]
                if person.is_dead:
                    continue
                all_dead = False

            if all_dead:
                break

    def _check_action(self):
        for persons_on_coordinate in self.__map.values():
            if len(persons_on_coordinate) > 1:
                self.fight(persons_on_coordinate)
            else:
                self.heal(persons_on_coordinate)

    def heal(self, persons_list: list['BasePerson']) -> None:
        for person in persons_list:
            if not person.need_healing:
                continue

            healing_volume = person.get_healing_volume()
            action_msg = f"пытался полечился, но что-то пошло не так"
            if healing_volume:
                action_msg = f"спокойно полечился на {healing_volume}"
                person.heal(healing_volume)
            person.log(action_msg)
            self.action_log.append(f"{person} {action_msg}")

    def fight(self, persons_list: list['BasePerson']) -> None:
        alive_persons = []
        dead_persons = []
        for person in persons_list:
            if person.is_dead:
                dead_persons.append(person)
            else:
                alive_persons.append(person)

        if len(alive_persons) == 0:
            return

        if len(alive_persons) == 1:
            looted = 0
            for dead_person in dead_persons:
                if dead_person.uuid not in self.looted_bodies:
                    looted += 1
                    self.looted_bodies.append(dead_person.uuid)
            if looted == 0:
                return
            person = alive_persons[0]
            self.action_log.append(f"{person} обыскал {plural(looted, ['тело','тела','тел'])}")
            person.add_experience(10*looted)
            return

        if roll_the_dice(20) >= 20:
            self.action_log.append(f"встретились {plural(len(alive_persons), ['разведчик','разведчика','разведчиков'])}, но все закончилсоь хорошо")
            for person in alive_persons:
                self.action_log.append(f"{person} был рад встрече")
                person.add_experience(10)
            return

        active_person_list = []
        for person in alive_persons:
            person.select_target(alive_persons)
            if person.target:
                active_person_list.append(person)

        if len(active_person_list) == 0:
            return

        self.action_log.append(
            f"встретились {plural(len(active_person_list), ['разведчик', 'разведчика', 'разведчиков'])}")
        active_person_list.sort(key=lambda p: p.get_initiative())

        while len(active_person_list) > 1:
            __active_person_list = []
            for person in active_person_list:
                if person.is_dead:
                    continue

                if person.stunned:
                    person.stunned = False
                    __active_person_list.append(person)
                    continue

                if not person.target or person.target.is_dead:
                    person.select_target(alive_persons)
                    if not person.target:
                        continue

                if person.hack(person.target):
                    person.target.stunned = True
                    action_msg = f"взломал системы {person.target}"
                    person.log(action_msg)
                    self.action_log.append(f"{person} {action_msg}")

                if person.attack(person.target):
                    damage_value = person.get_damage_volume()
                    if damage_value > 0:
                        person.target.hit(damage_value)
                        action_msg = f"наносит {damage_value} урона по {person.target}"
                        person.log(action_msg)
                        person.target.log(f"получает {damage_value} урона от {person}")
                        self.action_log.append(f"{person} {action_msg}")
                    else:
                        action_msg = f"не смог пробить защиту {person.target}"
                        person.log(action_msg)
                        person.target.log(f"не получает урона от {person}")
                        self.action_log.append(f"{person} {action_msg}")
                else:
                    action_msg = f"промахнулся по {person.target}"
                    person.log(action_msg)
                    self.action_log.append(f"{person} {action_msg}")

                if person.target.is_dead:
                    if person.target in __active_person_list:
                        __active_person_list.remove(person.target)
                    person.add_experience(100)
                    person.kills.append(person.target)
                    person.target.killed_by = person
                    action_msg = f"убивает {person.target}"
                    person.target.log(f"умирает от рук {person}")
                    self.action_log.append(f"{person} {action_msg}")

                __active_person_list.append(person)

            active_person_list = __active_person_list

    def move_person(self, person: 'BasePerson', x: int, y: int) -> None:
        if person.is_dead:
            return

        new_coordinate_key = f"{x}::{y}"
        old_coordinate_key = None
        if person.position_x and person.position_y:
            old_coordinate_key = f"{person.position_x}::{person.position_y}"

        if new_coordinate_key == old_coordinate_key:
            return

        if new_coordinate_key not in self.__map:
            self.__map[new_coordinate_key] = []

        if old_coordinate_key and old_coordinate_key in self.__map:
            self.__map[old_coordinate_key].remove(person)

        person.position_x = x
        person.position_y = y
        self.__map[new_coordinate_key].append(person)
