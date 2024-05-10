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
    max_cycles: int
    action_log: List[str]
    distances_dict: Dict[str, int]

    MAX_DISTANCE = 100

    def __init__(self, max_cycles: int) -> None:
        self.persons = {}
        self.users = []
        self.bots = []
        self.max_cycles = max_cycles
        self.action_log = []
        self.distances_dict = {}

        self.__meets = {}

    @classmethod
    def create_for_users(cls, robots_list: list["Robot"]) -> "StandartRaid":
        max_level = 1
        persons = []
        for robot in robots_list:
            person = PlayerPerson.create(robot)
            max_level = max(max_level, person.level)
            persons.append(person)

        max_cycles = max_level * 10
        raid = cls(
            max_cycles=max_cycles,
        )
        for person in persons:
            raid.join(person)

        raid_bots = 0
        for _ in range(len(robots_list)):
            raid_bots += roll_the_dice(5)
        for _ in range(raid_bots):
            bot = BotPerson.create(max_level)
            raid.join(bot)

        return raid

    def __str__(self) -> str:
        return f"Raid"

    def __repr__(self) -> str:
        return f"Raid"

    def join(self, person: BasePerson) -> None:
        self.persons[person.uuid] = person
        if isinstance(person, PlayerPerson):
            if person.uuid not in self.users:
                self.users.append(person.uuid)
        if isinstance(person, BotPerson):
            if person.uuid not in self.bots:
                self.bots.append(person.uuid)

    def play(self) -> None:
        for person_1 in self.persons.values():
            for person_2 in self.persons.values():
                if person_1.uuid == person_2.uuid:
                    continue
                initial_distance = (self.MAX_DISTANCE // 2) - roll_the_dice(20)
                self._set_distance(person_1=person_1, person_2=person_2, value=initial_distance)

        for _ in range(self.max_cycles):
            for person in self.persons.values():
                self.move_person(person=person)

            random.shuffle(self.users)

            all_dead = True

            for user_key in self.users:
                person = self.persons[user_key]
                if person.is_dead:
                    continue

                all_dead = False

                met_persons = self._get_met_persons(person)

                if len(met_persons) == 0:
                    if not person.need_healing:
                        continue

                    healing_volume = person.get_healing_volume()
                    action_msg = f"пытался полечился, но что-то пошло не так"
                    if healing_volume:
                        action_msg = f"спокойно полечился на {healing_volume}"
                        person.heal(healing_volume)
                    person.log(action_msg)
                    self.action_log.append(f"{person} {action_msg}")
                    continue

                len_met_persons = len(met_persons)
                action_msg = f"замечает {plural(len_met_persons, ['силуэт','силуэта','силуэтов'])}"
                person.log(action_msg)
                self.action_log.append(f"{person} {action_msg}")

                for met_person in met_persons:
                    if met_person.group == person.group:
                        action_msg = f"встретил союзника {met_person}"
                        person.log(action_msg)
                        met_person.log(f"наткнулся на союзника {person}")
                        self.action_log.append(f"{person} {action_msg}")
                        person.add_experience(10)
                        met_person.add_experience(10)
                        continue
                    self.fight(person, met_person)

            if all_dead:
                break

    def _get_met_persons(self, person: BasePerson) -> List[BasePerson]:
        if not isinstance(person, PlayerPerson):
            return []

        if person.is_dead:
            return []

        if person.uuid not in self.__meets:
            self.__meets[person.uuid] = {}

        already_met = self.__meets[person.uuid]
        meet_now: List[BasePerson] = []

        persons_keys = list(self.persons.keys())
        random.shuffle(persons_keys)

        for person_key in persons_keys:
            other_person = self.persons[person_key]

            if other_person == person or other_person.is_dead:
                continue

            distance = self._get_distance(person_1=person, person_2=other_person)
            vision = 20 + BasePerson.get_ability_modifier(person.wisdom)

            if distance > vision:
                continue

            meet_now.append(other_person)

            if other_person.uuid not in already_met:
                already_met[other_person.uuid] = 0
            already_met[other_person.uuid] += 1

            if other_person.uuid not in self.__meets:
                self.__meets[other_person.uuid] = {}
            if person.uuid not in self.__meets[other_person.uuid]:
                self.__meets[other_person.uuid][person.uuid] = 0
            self.__meets[other_person.uuid][person.uuid] += 1

        return meet_now

    def fight(self, person_1: BasePerson, person_2: BasePerson) -> None:
        if person_1.is_dead or person_2.is_dead:
            return

        if isinstance(person_1, PlayerPerson) and isinstance(person_2, PlayerPerson):
            dice_value = roll_the_dice(20) + BasePerson.get_ability_modifier(person_1.charisma)
            if dice_value >= 20:
                self.action_log.append(f"{person_1} и {person_2} разошлись миром")
                person_1.add_experience(100)
                person_2.add_experience(100)
                current_distance = self._get_distance(person_1=person_1, person_2=person_2)
                self._set_distance(person_1=person_1, person_2=person_2, value=current_distance + 30)
                return

        while person_1.is_alive and person_2.is_alive:
            if person_1.get_initiative() > person_2.get_initiative():
                q = [[person_1, person_2], [person_2, person_1]]
            else:
                q = [[person_2, person_1], [person_1, person_2]]
            for p1, p2 in q:
                if p1.attack(p2):
                    if self._one_hit_another(p1, p2):
                        break
                else:
                    action_msg = f"промахнулся по {p2}"
                    p1.log(action_msg)
                    self.action_log.append(f"{p1} {action_msg}")

    def _one_hit_another(self, person_1: 'BasePerson', person_2: 'BasePerson') -> bool:
        damage_value = person_1.get_damage_volume()
        person_2.hit(damage_value)

        action_msg = f"наносит {damage_value} урона по {person_2}"
        person_1.log(action_msg)
        person_2.log(f"получает {damage_value} урона от {person_1}")
        self.action_log.append(f"{person_1} {action_msg}")

        if person_2.is_dead:
            person_1.add_experience(100)
            person_1.kills.append(person_2)
            person_2.killed_by = person_1
            action_msg = f"убивает {person_2}"
            person_2.log(f"умирает от рук {person_1}")
            self.action_log.append(f"{person_1} {action_msg}")
            if person_1.health * 2 > person_1.max_health:
                action_msg = f"спокойно пережил схватку"
            else:
                action_msg = f"едва уцелел"
            person_1.log(action_msg)
            self.action_log.append(f"{person_1} {action_msg}")
            return True
        return False

    def move_person(self, person: 'BasePerson') -> None:
        if person.is_dead:
            return

        for other_person in self.persons.values():
            current_distance = self._get_distance(person_1=person, person_2=other_person)
            if not current_distance:
                continue
            change_value = person.speed
            change_direction = -1
            if roll_the_dice(6) > 3:
                change_direction = 1
            current_distance += change_value * change_direction
            self._set_distance(person_1=person, person_2=other_person, value=current_distance)

    def _get_distance(self, person_1: 'BasePerson', person_2: 'BasePerson') -> Union[int, None]:
        if person_1.is_dead or person_2.is_dead:
            return

        key = self.__get_distance_key(person_1=person_1, person_2=person_2)
        if key not in self.distances_dict:
            self.distances_dict[key] = self.MAX_DISTANCE

        return self.distances_dict[key]

    def _set_distance(self, person_1: 'BasePerson', person_2: 'BasePerson', value: int) -> None:
        if person_1.is_dead or person_2.is_dead:
            return

        if value < 0:
            value = 0

        key = self.__get_distance_key(person_1=person_1, person_2=person_2)
        if key not in self.distances_dict:
            self.distances_dict[key] = self.MAX_DISTANCE

        self.distances_dict[key] = min(self.MAX_DISTANCE, value)

    def __get_distance_key(self, person_1: 'BasePerson', person_2: 'BasePerson') -> str:
        key_list = [str(person_1.uuid), str(person_2.uuid)]
        key_list.sort()
        return ":".join(key_list)
