import random


def roll_the_dice(num: int = 20) -> int:
    return random.randint(1, num)
