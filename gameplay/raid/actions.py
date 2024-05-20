import copy
import sys
from typing import Optional

from app.utils import plural
from gameplay.person import BasePerson


class Action():
    actor = BasePerson
    action = str
    value = int
    target = Optional[BasePerson]

    def __init__(
            self,
            actor: Optional[BasePerson] = None,
            value: Optional[int] = None,
            target: Optional[BasePerson] = None
    ):
        self.actor = copy.deepcopy(actor) if actor is not None else None
        self.action = self.__class__.__name__.upper()
        self.value = value
        self.target = copy.deepcopy(target) if target is not None else None

    def __str__(self):
        result = self.action
        if self.value is not None:
            result = f"{result} {self.value}"
        if self.actor is not None:
            result = f"{self.actor} {result}"
        if self.target is not None:
            result = f"{result} {self.target}"
        return result

    def to_json(self):
        result = {
            "action": self.action,
        }
        if self.value is not None:
            result["value"] = self.value
        if self.actor is not None:
            result["actor"] = self.actor.to_json()
        if self.target is not None:
            result["target"] = self.target.to_json()
        return result

    @classmethod
    def from_json(cls, json_dict):
        class_name = json_dict['action'].capitalize()
        params = {}
        if 'actor' in json_dict and json_dict['actor'] is not None:
            params["actor"] = BasePerson.from_json(json_dict['actor'])
        if 'value' in json_dict and json_dict['value'] is not None:
            params["value"] = json_dict['value']
        if 'target' in json_dict and json_dict['target'] is not None:
            params["target"] = BasePerson.from_json(json_dict['target'])
        return getattr(sys.modules[__name__], class_name)(**params)


class Hit(Action):
    plural_list = ["урон", "урона", "урона"]

    def __init__(self, actor: BasePerson, value: int, target: BasePerson):
        super().__init__(
            actor=actor,
            value=value,
            target=target
        )

    def __str__(self):
        if self.value == 0:
            return f"{self.actor} не смог повредить {self.target}"
        if self.target.is_dead:
            return f"{self.actor} убивает {self.target} нанеся {plural(self.value, self.plural_list)}"
        return f"{self.actor} попадает по {self.target} и наносит {plural(self.value, self.plural_list)}"


class Heal(Action):
    plural_list = ["единицу", "единицы", "единиц"]

    def __init__(self, actor: BasePerson, value: int):
        super().__init__(
            actor=actor,
            value=value,
        )

    def __str__(self):
        if self.value == 0:
            return f"{self.actor} пытался в ремонт, но ничего не вышло"
        return f"{self.actor} восстанавливает {plural(self.value, self.plural_list)} прочности"


class Met(Action):
    plural_list = ["разведчик", "разведчика", "разведчиков"]

    def __init__(self, value: int):
        super().__init__(
            value=value,
        )

    def __str__(self):
        return f"встречаются {plural(self.value, self.plural_list)}"


class Hacked(Action):
    plural_list = ["ход", "хода", "ходов"]

    def __init__(self, actor: BasePerson, target: BasePerson, value: int = 1):
        super().__init__(
            actor=actor,
            value=value,
            target=target,
        )

    def __str__(self):
        return f"{self.actor} взламывает системы {self.target}, парализуя его на {plural(self.value, self.plural_list)}"


class Missed(Action):
    def __init__(self, actor: BasePerson, target: BasePerson):
        super().__init__(
            actor=actor,
            target=target,
        )

    def __str__(self):
        return f"{self.actor} промахивается по {self.target}"
