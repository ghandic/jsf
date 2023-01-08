import random

LOREM = """Lorem ipsum dolor sit amet consectetur adipisicing elit.
Hic molestias, esse veniam placeat officiis nobis architecto modi
possimus reiciendis accusantium exercitationem quas illum libero odit magnam,
reprehenderit ipsum, repellendus culpa!""".split()


def random_fixed_length_sentence(_min: int = 0, _max: int = 50) -> str:
    output = ""
    while len(output) < _max:
        remaining = _max - len(output)
        valid_words = list(filter(lambda s: len(s) < remaining, LOREM))
        if len(valid_words) == 0:
            break
        output += random.choice(valid_words) + " "
        if len(output) > _min and random.uniform(0, 1) > 0.9:
            break
    return output.strip()
