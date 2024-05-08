import random


def roll_the_dice(num: int = 20) -> int:
    return random.randint(1, num)


def roll_ability_dice() -> int:
    dices = [roll_the_dice(6) for _ in range(4)]
    dices.remove(min(dices))
    return sum(dices)
