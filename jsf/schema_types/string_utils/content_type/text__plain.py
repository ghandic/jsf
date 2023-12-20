import random
import string


def random_fixed_length_sentence(_min: int = 0, _max: int = 50) -> str:
    if _min > _max:
        raise ValueError("'_max' should be greater than '_min'")  # pragma: no cover
    return "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(_min, _max)))
