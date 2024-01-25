import random

LOREM = """Lorem ipsum dolor sit amet consectetur adipisicing elit.
Hic molestias, esse veniam placeat officiis nobis architecto modi
possimus reiciendis accusantium exercitationem quas illum libero odit magnam,
reprehenderit ipsum, repellendus culpa! Nullam vehicula ipsum a arcu cursus vitae congue.
Enim nec dui nunc mattis enim ut tellus.""".split()


def random_fixed_length_sentence(_min: int = 0, _max: int = 50) -> str:
    if _min > _max:
        raise ValueError("'_max' should be greater than '_min'")  # pragma: no cover
    output = ""
    while True:
        remaining = _max - len(output)
        valid_words = list(filter(lambda s: len(s) <= remaining, LOREM))
        if len(valid_words) == 0:
            break
        if len(output) >= _min and random.uniform(0, 1) > 0.9:
            break
        output += random.choice(valid_words) + " "
    output = output.strip()
    if len(output) < _min:
        output = output + "."
    return output
