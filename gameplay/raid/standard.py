import random

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

        raid_bots = random.randint(1, 10)
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
                if player.is_dead():
                    continue
                all_dead = False

                met_persons = self.get_met_persons(player)

                if not met_persons:
                    if player.health < player.max_health:
                        heal_value = random.randint(10, 20)
                        player.heal(heal_value)
                        self.action_log.append(f"{player} спокойно похилился на {heal_value}, здоровье {player.health}")
                    continue

                self.action_log.append(f"{player} встречает {len(met_persons)}")
                for met_person in met_persons:
                    if met_person.group != player.group:
                        self.fight(player, met_person)
                    else:
                        self.action_log.append(f"{player} встретил союзника {met_person}")
                        player.add_experience(150)
                        met_person.add_experience(150)

            if all_dead:
                break

    def get_met_persons(self, person: BasePerson) -> List[BasePerson]:
        if isinstance(person, PlayerPerson):
            met_players = self.__get_met_players(person)
            met_bots = self.__get_met_bots(person)
            return [*met_players, *met_bots]

        return []

    def __get_met_players(self, player: BasePerson) -> List[PlayerPerson]:
        if random.random() > 0.2:
            return []

        already_met = self.__meets.get(player.uuid, {})
        met_players: List[PlayerPerson] = []

        for other_player in self.players.values():
            if other_player != player and other_player.is_alive():
                chance_to_meet = 0.2 - already_met.get(other_player.uuid, 0) * 0.05
                if random.random() < chance_to_meet:
                    met_players.append(other_player)
                    if other_player.uuid not in already_met:
                        already_met[other_player.uuid] = 0
                    already_met[other_player.uuid] += 1

        return met_players

    def __get_met_bots(self, player: BasePerson) -> List[BotPerson]:
        if random.random() > 0.3:
            return []

        already_met = self.__meets.get(player.uuid, {})
        met_bots: List[BotPerson] = []

        for bot in self.bots.values():
            if bot.is_alive():
                chance_to_meet = 0.3 - already_met.get(bot.uuid, 0) * 0.05
                if random.random() < chance_to_meet:
                    met_bots.append(bot)
                    if bot.uuid not in already_met:
                        already_met[bot.uuid] = 0
                    already_met[bot.uuid] += 1

        return met_bots

    def fight(self, person_1: BasePerson, person_2: BasePerson) -> None:
        peaceful_ending = 1
        if isinstance(person_1, PlayerPerson) or isinstance(person_2, PlayerPerson):
            peaceful_ending = 0
            if isinstance(person_1, PlayerPerson) and isinstance(person_2, PlayerPerson):
                peaceful_ending = random.random() > 0.5

        if peaceful_ending:
            self.action_log.append(f"{person_1} и {person_2} разошлись миром")
            person_1.add_experience(100)
            person_1.heal(10)
            self.action_log.append(f"{person_1} подлечился на 10, здоровье {person_1.health}")
            person_2.add_experience(100)
            person_2.heal(10)
            self.action_log.append(f"{person_2} подлечился на 10, здоровье {person_2.health}")
            return

        while person_1.is_alive() and person_2.is_alive():
            hit_value = person_2.get_damage_value()
            if hit_value:
                person_1.hit(hit_value)
                self.action_log.append(f"{person_2} урон по {person_1} в размере {hit_value}")

            hit_value = person_1.get_damage_value()
            if hit_value:
                person_2.hit(hit_value)
                self.action_log.append(f"{person_1} урон по {person_2} в размере {hit_value}")

        if person_1.is_dead():
            self.action_log.append(f"{person_1} погибает от рук {person_2}")
            person_1.killed_by = person_2
            person_2.kills.append(person_1)
        else:
            self.action_log.append(f"{person_1} едва уцелел, здоровье {person_1.health}")
            person_1.add_experience(200)

        if person_2.is_dead():
            self.action_log.append(f"{person_2} погибает от рук {person_1}")
            person_2.killed_by = person_1
            person_1.kills.append(person_2)
        else:
            self.action_log.append(f"{person_2} едва уцелел, здоровье {person_2.health}")
            person_2.add_experience(200)
