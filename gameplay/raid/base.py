import random

from app.utils import plural
from gameplay.dices import roll_the_dice
from gameplay.person import BasePerson, BotPerson, PlayerPerson
from typing import Dict, List, Union
from robots.models import Robot
from raids.models import Raid


class BaseRaid:
    persons: Dict[str, BasePerson]
    users: List[str]
    bots: List[str]
    action_log: List[str]
    max_x: int
    max_y: int
    max_rounds: int
    current_round: int
    __map: dict[str, list[BasePerson]]
    __map_by_rounds: list[dict[str, list[BasePerson]]]

    def __init__(self, max_x: int, max_y: int, max_rounds: int, current_round: int = 1) -> None:
        self.persons = {}
        self.users = []
        self.bots = []
        self.max_x = max_x
        self.max_y = max_y
        self.max_rounds = max_rounds
        self.current_round = current_round
        self.action_log = []

        self.__map = {}
        self.__map_by_rounds = []

    @classmethod
    def create_for_user(cls, robot: "Robot") -> "BaseRaid":
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

    @classmethod
    def create_for_raid(cls, raid: "Raid") -> "BaseRaid":
        gameplay_raid = cls(**raid.config_state)
        for robot_dict in raid.users_state:
            person = PlayerPerson.from_json(robot_dict)
            gameplay_raid.join(person)

        for bot_dict in raid.bots_state:
            bot = BotPerson.from_json(bot_dict)
            gameplay_raid.join(bot)

        return gameplay_raid

    def __str__(self) -> str:
        return f"Raid"

    def __repr__(self) -> str:
        return f"Raid"

    def get_config_json(self):
        return {
            "max_x": self.max_x,
            "max_y": self.max_y,
            "max_rounds": self.max_rounds,
            "current_round": self.current_round,
        }

    def join(self, person: BasePerson) -> None:
        if not person.position_x and not person.position_y:
            person.move(
                x=random.randint(1, self.max_x),
                y=random.randint(1, self.max_y)
            )
        self.map_update_person(person)
        self.persons[person.uuid] = person
        if isinstance(person, PlayerPerson):
            if person.uuid not in self.users:
                self.users.append(person.uuid)
        if isinstance(person, BotPerson):
            if person.uuid not in self.bots:
                self.bots.append(person.uuid)

    @property
    def is_ended(self):
        if self.current_round >= self.max_rounds:
            return True
        return False

    def next_round(self):
        self.current_round += 1
        self._check_action()
        all_dead = True
        for user_key in self.users:
            person = self.persons[user_key]
            person.reset_action_points()
            if person.is_dead:
                continue
            all_dead = False
        if all_dead:
            self.current_round = self.max_rounds

    def move_user(self, user_uuid, x, y) -> bool:
        person = self.persons[user_uuid]
        if not person.can_move:
            return False
        person.move(x=x, y=y)
        self.map_update_person(person)
        self._check_action()

        if not person.can_move:
            self.move_bots()
            self.next_round()

    def move_bots(self) -> None:
        for bot_key in self.bots:
            bot = self.persons[bot_key]
            bot.reset_action_points()
            while bot.can_move:
                new_x_min = max(bot.position_x - 1, 1)
                new_x_max = min(bot.position_x + 1, self.max_x)
                new_y_min = max(bot.position_y - 1, 1)
                new_y_max = min(bot.position_y + 1, self.max_y)
                bot.move(x=random.choice([new_x_min, new_x_max]), y=random.choice([new_y_min, new_y_max]))
                self.map_update_person(bot)
                self._check_action()

    def _check_action(self):
        for persons_on_coordinate in self.__map.values():
            if len(persons_on_coordinate) > 1:
                all_acted = True
                for person in persons_on_coordinate:
                    if not person.acted:
                        all_acted = False
                if not all_acted:
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
            self.action_log.append(f"{person} {action_msg}")

    def fight(self, persons_list: list['BasePerson']) -> None:
        alive_persons = []
        dead_persons = []
        for person in persons_list:
            if person.is_dead:
                dead_persons.append(person)
            else:
                alive_persons.append(person)
                person.acted = True

        if len(alive_persons) == 0:
            return

        if len(alive_persons) == 1:
            looted = 0
            for dead_person in dead_persons:
                if not dead_person.looted:
                    looted += 1
                    dead_person.loot()
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

                person.ability_checks()
                if person.stunned:
                    __active_person_list.append(person)
                    continue

                if not person.target:
                    person.select_target(alive_persons)
                    if not person.target:
                        continue

                person_target = self.persons[person.target]
                if person_target.is_dead:
                    person.select_target(alive_persons)
                    if not person.target:
                        continue
                    person_target = self.persons[person.target]

                if not person_target.stunned and person.hack_check(person_target):
                    person_target.stun()
                    action_msg = f"взломал системы {person_target}"
                    self.action_log.append(f"{person} {action_msg}")

                if person.attack_check(person_target):
                    damage_value = person.get_damage_volume()
                    if damage_value > 0:
                        person_target.hit(damage_value)
                        action_msg = f"наносит {damage_value} урона по {person_target}"
                        self.action_log.append(f"{person} {action_msg}")
                    else:
                        action_msg = f"не смог пробить защиту {person_target}"
                        self.action_log.append(f"{person} {action_msg}")
                else:
                    action_msg = f"промахнулся по {person_target}"
                    self.action_log.append(f"{person} {action_msg}")

                if person_target.is_dead:
                    if person_target in __active_person_list:
                        __active_person_list.remove(person_target)
                    person.add_experience(100)
                    person.kills.append(person_target.uuid)
                    person_target.killed_by = person.uuid
                    action_msg = f"убивает {person_target}"
                    self.action_log.append(f"{person} {action_msg}")

                __active_person_list.append(person)

            active_person_list = __active_person_list

    def map_update_person(self, person: 'BasePerson') -> None:
        if person.is_dead:
            return

        new_coordinate_key = f"{person.position_x}::{person.position_y}"
        old_coordinate_key = None
        if person.trails:
            prev_point = person.trails[-1]
            old_coordinate_key = f"{prev_point[0]}::{prev_point[1]}"

        if new_coordinate_key == old_coordinate_key:
            return

        if new_coordinate_key not in self.__map:
            self.__map[new_coordinate_key] = []

        if old_coordinate_key and old_coordinate_key in self.__map:
            try:
                self.__map[old_coordinate_key].remove(person)
            except ValueError:
                pass

        self.__map[new_coordinate_key].append(person)
