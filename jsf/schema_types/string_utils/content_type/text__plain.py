import random
import string
from typing import Optional


def random_fixed_length_sentence(_min: Optional[int] = 0, _max: Optional[int] = 50) -> str:
    if _min > _max:
        raise ValueError("'_max' should be greater than '_min'")  # pragma: no cover
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(_min, _max)))
