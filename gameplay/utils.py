from gameplay.consts import LEVEL_PROGRESSION


def get_level_at_experience(experience: int) -> int:
    for level, threshold in enumerate(LEVEL_PROGRESSION):
        if experience >= threshold:
            continue
        return level - 1
    return 20
