import re
import random
from datetime import timezone
from dataclasses import dataclass
from typing import Callable, Optional, List, Union, Dict, Callable, Any

import rstr
from faker import Faker


from .base import BaseSchema, ProviderNotSetException

faker = Faker()

FRAGMENT = "[a-zA-Z][a-zA-Z0-9+-.]*"
URI_PATTERN = f"https?://{{hostname}}(?:{FRAGMENT})+"
PARAM_PATTERN = "(?:\\?([a-z]{1,7}(=\\w{1,5})?&){0,3})?"

LOREM = """Lorem ipsum dolor sit amet consectetur adipisicing elit. 
Hic molestias, esse veniam placeat officiis nobis architecto modi 
possimus reiciendis accusantium exercitationem quas illum libero odit magnam, 
reprehenderit ipsum, repellendus culpa!""".split()

format_map: Dict[str, Callable] = {
    "date-time": lambda: faker.date_time(timezone.utc).isoformat(),
    "time": lambda: faker.date_time(timezone.utc).isoformat().split("T")[1],
    "date": lambda: faker.date_time(timezone.utc).isoformat().split("T")[0],
    "email": faker.email,
    "idn-email": faker.email,
    "hostname": faker.hostname,
    "idn-hostname": faker.hostname,
    "ipv4": faker.ipv4,
    "ipv6": faker.ipv6,
    "uri": faker.uri,
    "uri-reference": lambda: faker.uri() + rstr.xeger(PARAM_PATTERN),
    "iri": faker.uri,
    "iri-reference": lambda: faker.uri() + rstr.xeger(PARAM_PATTERN),
    "uri-template": lambda: rstr.xeger(
        URI_PATTERN.format(hostname=re.escape(faker.hostname())).replace("(?:", "(?:/\\{[a-z][:a-zA-Z0-9-]*\\}|")
    ),
    "json-pointer": lambda: rstr.xeger(f"(/(?:${FRAGMENT.replace(']*', '/]*')}|~[01]))+"),
    "relative-json-pointer": lambda: rstr.xeger(
        f"(/(?:${FRAGMENT.replace(']*', '/]*')}|~[01]))+"
    ),  # NOTE: Would need access to whole root object to mock properly
    "uuid": faker.uuid4,
}


def random_fixed_length_sentence(_min: int, _max: int) -> str:
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


@dataclass
class String(BaseSchema):
    minLength: Optional[float] = 0
    maxLength: Optional[float] = 50
    pattern: Optional[str] = re.compile(f".{{{minLength},{maxLength}}}")
    format: Optional[str] = None
    # enum: Optional[List[Union[str, int, float]]] = None  # NOTE: Not used - enums go to enum class

    def generate(self, state: Dict[str, Any]) -> Optional[str]:
        try:
            return str(super().generate(state))
        except ProviderNotSetException:
            format_map["regex"] = lambda: rstr.xeger(self.pattern)
            format_map["relative-json-pointer"] = lambda: random.choice(state["__all_json_paths__"])
            if format_map.get(self.format) is not None:
                return format_map[self.format]()
            return random_fixed_length_sentence(self.minLength, self.maxLength)

