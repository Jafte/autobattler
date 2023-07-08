import random

from gameplay.person import GameplayPersonBase, GameplayPersonBot, GameplayPersonPlayer
from typing import Dict, List
from raids.enums import RaidStatus
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from raids.models import UserRaid


class GameplayRaid:
    players: Dict[str, GameplayPersonPlayer]
    max_players: int
    bots: Dict[str, GameplayPersonBot]
    max_bots: int
    current_cycle: int
    max_cycles: int
    status: 'RaidStatus'
    action_log: List[str]

    __cycle_bots: List[str]
    __cycle_players: List[str]

    def __init__(self, max_players: int, max_bots: int, max_cycles: int) -> None:
        self.players = {}
        self.max_players = max_players
        self.bots = {}
        self.max_bots = max_bots
        self.current_cycle = 0
        self.max_cycles = max_cycles
        self.status = RaidStatus.NEW
        self.action_log = []

    @classmethod
    def create_from_user_raid(cls, user_raid: 'UserRaid') -> 'GameplayRaid':
        raid = cls(
            max_players=user_raid.rules.get('max_players', 5),
            max_bots=user_raid.rules.get('max_bots', 20),
            max_cycles=user_raid.rules.get('max_cycles', 100),
        )

        for model in user_raid.players.all():
            person = GameplayPersonPlayer.create(model)
            raid.join(person)

        raid_bots = random.randint(1, raid.max_bots)
        for _ in range(raid_bots):
            bot = GameplayPersonBot.create()
            raid.join(bot)

        return raid

    def __str__(self) -> str:
        return f"Raid [{self.status.name}]"

    def __repr__(self) -> str:
        return f"Raid [{self.status.name}]"

    def join(self, person: GameplayPersonBase) -> bool:
        if self.status != RaidStatus.NEW:
            return False

        if isinstance(person, GameplayPersonPlayer):
            return self.__join_player(person)
        if isinstance(person, GameplayPersonBot):
            return self.__join_bot(person)

        return False

    def __join_player(self, player: GameplayPersonPlayer) -> bool:
        if len(self.players) >= self.max_players:
            return False
        if player.uuid not in self.players:
            self.players[player.uuid] = player
        return True

    def __join_bot(self, bot: GameplayPersonBot) -> bool:
        if len(self.bots) >= self.max_bots:
            return False
        if bot.uuid not in self.bots:
            self.bots[bot.uuid] = bot
        return True

    def start(self) -> bool:
        if self.status != RaidStatus.NEW:
            return False

        self.status = RaidStatus.IN_PROGRESS

        return True

    def finish(self) -> bool:
        if self.status != RaidStatus.IN_PROGRESS:
            return False
        self.status = RaidStatus.FINISHED

        return True

    def play(self) -> None:
        if self.status != RaidStatus.IN_PROGRESS:
            return

        next_cycle = self.current_cycle + 1
        if next_cycle > self.max_cycles:
            self.finish()
            return

        self.current_cycle = next_cycle
        self.__cycle_bots = list(self.bots.keys())
        self.__cycle_players = list(self.players.keys())
        all_dead = True

        players_keys = list(self.players.keys())
        random.shuffle(players_keys)

        for players_key in players_keys:
            player = self.players[players_key]
            if not player.is_alive():
                continue

            all_dead = False
            met_persons = self.get_met_persons(player)

            if met_persons:
                pass
                self.action_log.append(f"{player} встречает {len(met_persons)} противников")
            else:
                if player.health < 100:
                    player.heal(random.randint(10, 20))
                    self.action_log.append(f"{player} спокойно похилился, здоровье {player.health}")

            for met_person in met_persons:
                self.fight(player, met_person)
                if not player.is_alive():
                    break

        if not all_dead:
            self.play()
        else:
            self.finish()

    def get_met_persons(self, person: GameplayPersonBase) -> List[GameplayPersonBase]:
        if isinstance(person, GameplayPersonPlayer):
            met_players = self.__get_met_players(person)
            met_bots = self.__get_met_bots(person)
            return [*met_players, *met_bots]

        return []

    def __get_met_players(self, player: GameplayPersonBase) -> List[GameplayPersonPlayer]:
        if random.random() > 0.2:
            return []

        met_players: List[GameplayPersonPlayer] = []

        for other_player_key in self.__cycle_players:
            other_player = self.players[other_player_key]
            if other_player != player and other_player.is_alive():
                if random.random() > 0.9:
                    met_players.append(other_player)

        for met_player_key in met_players:
            self.__cycle_players.remove(met_player_key.uuid)

        return met_players

    def __get_met_bots(self, player: GameplayPersonBase) -> List[GameplayPersonBot]:
        if random.random() > 0.3:
            return []

        met_bots: List[GameplayPersonBot] = []

        for bot_key in self.__cycle_bots:
            bot = self.bots[bot_key]
            if bot.is_alive():
                if random.random() > 0.7:
                    met_bots.append(bot)

        for met_bot in met_bots:
            self.__cycle_bots.remove(met_bot.uuid)

        return met_bots

    def fight(self, person_1: GameplayPersonBase, person_2: GameplayPersonBase) -> None:
        peaceful_ending = 1
        if isinstance(person_1, GameplayPersonPlayer) or isinstance(person_2, GameplayPersonPlayer):
            peaceful_ending = 0
            if isinstance(person_1, GameplayPersonPlayer) and isinstance(person_2, GameplayPersonPlayer):
                peaceful_ending = random.random() > 0.5

        if peaceful_ending:
            self.action_log.append(f"{person_1} и {person_2} разошлись миром")
            person_1.add_experience(100)
            person_1.heal(10)
            person_2.add_experience(100)
            person_2.heal(10)
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

        if not person_1.is_alive():
            person_1.killed_by = person_2.name
            self.action_log.append(f"{person_1} погибает от рук {person_2}")

        if not person_2.is_alive():
            person_2.killed_by = person_1.name
            self.action_log.append(f"{person_2} погибает от рук {person_1}")

        if person_1.is_alive():
            self.action_log.append(f"{person_1} едва уцелел, здоровье {person_1.health}")
            person_1.add_experience(200)

        if person_2.is_alive():
            self.action_log.append(f"{person_2} едва уцелел, здоровье {person_2.health}")
            person_2.add_experience(200)
