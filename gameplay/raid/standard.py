import random

from app.utils import plural
from gameplay.dices import roll_the_dice
from gameplay.person import BasePerson, BotPerson, PlayerPerson
from typing import Dict, List
from robots.models import Robot


class StandartRaid:
    players: Dict[str, PlayerPerson]
    bots: Dict[str, BotPerson]
    max_cycles: int
    action_log: List[str]

    def __init__(self, max_cycles: int) -> None:
        self.players = {}
        self.bots = {}
        self.max_cycles = max_cycles
        self.action_log = []

        self.__meets = {}

    @classmethod
    def create_for_users(cls, robots_list: list["Robot"]) -> "StandartRaid":
        raid = cls(
            max_cycles=100,
        )

        for robot in robots_list:
            person = PlayerPerson.create(robot)
            raid.join(person)

        min_bots = len(robots_list) * 2
        max_bots = min_bots * 3 + 1
        raid_bots = random.randint(min_bots, max_bots)
        for _ in range(raid_bots):
            bot = BotPerson.create()
            raid.join(bot)

        return raid

    def __str__(self) -> str:
        return f"Raid"

    def __repr__(self) -> str:
        return f"Raid"

    def join(self, person: BasePerson) -> bool:
        if isinstance(person, PlayerPerson):
            return self.__join_player(person)
        if isinstance(person, BotPerson):
            return self.__join_bot(person)

        return False

    def __join_player(self, player: PlayerPerson) -> bool:
        if player.uuid not in self.players:
            self.players[player.uuid] = player
        return True

    def __join_bot(self, bot: BotPerson) -> bool:
        if bot.uuid not in self.bots:
            self.bots[bot.uuid] = bot
        return True

    def play(self) -> None:
        for current_cycle in range(1, self.max_cycles + 1):
            players_keys = list(self.players.keys())
            random.shuffle(players_keys)

            all_dead = True

            for players_key in players_keys:
                player = self.players[players_key]
                if player.is_dead:
                    continue

                all_dead = False

                met_persons = self._get_met_persons(player)

                if len(met_persons) == 0:
                    if not player.need_healing:
                        continue

                    healing_volume = player.get_healing_volume()
                    player.heal(healing_volume)
                    action_msg = f"спокойно полечился на {healing_volume}"
                    player.log(action_msg)
                    self.action_log.append(f"{player} {action_msg}")
                    continue

                len_met_persons = len(met_persons)
                action_msg = f"замечает {plural(len_met_persons, ['силуэт','силуэта','силуэтов'])}"
                player.log(action_msg)
                self.action_log.append(f"{player} {action_msg}")

                for met_person in met_persons:
                    if met_person.group != player.group:
                        self.fight(player, met_person)
                        continue

                    if met_person.group == player.group:
                        action_msg = f"встретил союзника {met_person}"
                        player.log(action_msg)
                        met_person.log(f"наткнулся на союзника {player}")
                        self.action_log.append(f"{player} {action_msg}")
                        player.add_experience(10)
                        met_person.add_experience(10)

            if all_dead:
                break

    def _get_met_persons(self, person: BasePerson) -> List[BasePerson]:
        if isinstance(person, PlayerPerson):
            met_players = self.__get_met_players(person)
            met_bots = self.__get_met_bots()
            return [*met_players, *met_bots]

        return []

    def __get_met_players(self, player: BasePerson) -> List[PlayerPerson]:
        dice_value = roll_the_dice(20)
        if dice_value == 20:
            return []

        if player.uuid not in self.__meets:
            self.__meets[player.uuid] = {}

        already_met = self.__meets[player.uuid]
        met_players: List[PlayerPerson] = []

        for other_player in self.players.values():
            if other_player != player and other_player.is_alive:
                dice_value = roll_the_dice(6) + already_met.get(other_player.uuid, 0)
                if dice_value < 4:
                    met_players.append(other_player)
                    if other_player.uuid not in already_met:
                        already_met[other_player.uuid] = 0
                    if other_player.uuid not in self.__meets:
                        self.__meets[other_player.uuid] = {}
                    if player.uuid not in self.__meets[other_player.uuid]:
                        self.__meets[other_player.uuid][player.uuid] = 0
                    already_met[other_player.uuid] += 1
                    self.__meets[other_player.uuid][player.uuid] += 1

        return met_players

    def __get_met_bots(self) -> List[BotPerson]:
        dice_value = roll_the_dice(20)
        if dice_value >= 19:
            return []

        met_bots: List[BotPerson] = []

        for bot in self.bots.values():
            if bot.is_alive:
                dice_value = roll_the_dice(10)
                if dice_value < 6:
                    met_bots.append(bot)

        return met_bots

    def fight(self, person_1: BasePerson, person_2: BasePerson) -> None:
        if person_1.is_dead or person_2.is_dead:
            return

        if isinstance(person_1, PlayerPerson) and isinstance(person_2, PlayerPerson):
            dice_value = roll_the_dice(20)
            if dice_value == 20:
                self.action_log.append(f"{person_1} и {person_2} разошлись миром")
                person_1.add_experience(100)
                person_2.add_experience(100)
                return

        while person_1.is_alive and person_2.is_alive:
            if person_1.get_initiative() > person_2.get_initiative():
                if person_1.attack(person_2):
                    if self._one_hit_another(person_1, person_2):
                        break
                else:
                    action_msg = f"промахнулся по {person_2}"
                    person_1.log(action_msg)
                    self.action_log.append(f"{person_1} {action_msg}")

                if person_2.attack(person_1):
                    if self._one_hit_another(person_2, person_1):
                        break
                else:
                    action_msg = f"промахнулся по {person_1}"
                    person_2.log(action_msg)
                    self.action_log.append(f"{person_2} {action_msg}")
            else:
                if person_2.attack(person_1):
                    if self._one_hit_another(person_2, person_1):
                        break
                else:
                    action_msg = f"промахнулся по {person_1}"
                    person_2.log(action_msg)
                    self.action_log.append(f"{person_2} {action_msg}")

                if person_1.attack(person_2):
                    if self._one_hit_another(person_1, person_2):
                        break
                else:
                    action_msg = f"промахнулся по {person_2}"
                    person_1.log(action_msg)
                    self.action_log.append(f"{person_1} {action_msg}")

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
            action_msg = f"едва уцелел"
            person_1.log(action_msg)
            self.action_log.append(f"{person_1} {action_msg}")
            return True
        return False
