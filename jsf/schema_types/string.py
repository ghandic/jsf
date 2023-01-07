import base64
import logging
import quopri
import random
import re
from datetime import timezone
from enum import Enum
from typing import Any, Callable, Dict, Optional

import rstr
from faker import Faker

from jsf.schema_types.base import BaseSchema, ProviderNotSetException

logger = logging.getLogger()
faker = Faker()

FRAGMENT = "[a-zA-Z][a-zA-Z0-9+-.]*"
URI_PATTERN = f"https?://{{hostname}}(?:{FRAGMENT})+"
PARAM_PATTERN = "(?:\\?([a-z]{1,7}(=\\w{1,5})?&){0,3})?"

LOREM = """Lorem ipsum dolor sit amet consectetur adipisicing elit.
Hic molestias, esse veniam placeat officiis nobis architecto modi
possimus reiciendis accusantium exercitationem quas illum libero odit magnam,
reprehenderit ipsum, repellendus culpa!""".split()


def temporal_duration(
    positive: bool = True,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    milliseconds: int = 0,
    microseconds: int = 0,
    nanoseconds: int = 0,
) -> str:
    duration = "P"
    # dur-date
    if years != 0:
        duration = f"{duration}{years}Y"
    if months != 0:
        duration = f"{duration}{months}M"
    if weeks != 0:
        duration = f"{duration}{weeks}W"
    if days != 0:
        duration = f"{duration}{days}D"

    # dur-time
    if hours + minutes + seconds + milliseconds + microseconds + nanoseconds != 0:
        duration = f"{duration}T"
    if hours != 0:
        duration = f"{duration}{hours}H"
    if minutes != 0:
        duration = f"{duration}{minutes}M"
    if seconds + milliseconds + microseconds + nanoseconds != 0:
        if remainder := "".join(
            str(part) for part in [milliseconds, microseconds, nanoseconds] if part
        ):
            seconds = f"{seconds}.{remainder}"
        duration = f"{duration}{seconds}S"

    # Case where there was no duration specified, still need to output valid format string
    if duration == "P":
        duration = "PT0S"

    # direction
    if not positive:
        duration = f"-{duration}"

    return duration


def mostly_zero_randint(min, max):
    return 0 if random.random() > 0.8 else random.randint(min, max)


def fake_duration():
    generic_max = 1000
    return temporal_duration(
        positive=random.random() > 0.5,
        years=mostly_zero_randint(0, generic_max),
        months=mostly_zero_randint(0, generic_max),
        weeks=mostly_zero_randint(0, generic_max),
        days=mostly_zero_randint(0, generic_max),
        hours=mostly_zero_randint(0, generic_max),
        minutes=mostly_zero_randint(0, generic_max),
        seconds=mostly_zero_randint(0, generic_max),
        milliseconds=mostly_zero_randint(0, 999),
        microseconds=mostly_zero_randint(0, 999),
        nanoseconds=mostly_zero_randint(0, 999),
    )


format_map: Dict[str, Callable] = {
    "date-time": lambda: faker.date_time(timezone.utc).isoformat(),
    "time": lambda: faker.date_time(timezone.utc).isoformat().split("T")[1],
    "date": lambda: faker.date_time(timezone.utc).isoformat().split("T")[0],
    "duration": fake_duration,
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
        URI_PATTERN.format(hostname=re.escape(faker.hostname())).replace(
            "(?:", "(?:/\\{[a-z][:a-zA-Z0-9-]*\\}|"
        )
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


class ContentEncoding(str, Enum):
    SEVEN_BIT = "7-bit"
    EIGHT_BIT = "8-bit"
    BINARY = "binary"
    QUOTED_PRINTABLE = "quoted-printable"
    BASE16 = "base-16"
    BASE32 = "base-32"
    BASE64 = "base-64"


def binary_encoder(string: str) -> str:
    return "".join(format(x, "b") for x in bytearray(string, "utf-8"))


def bytes_str_repr(b: bytes) -> str:
    return repr(b)[2:-1]


def seven_bit_encoder(string: str) -> str:
    return bytes_str_repr(string.encode("utf-7"))


def eight_bit_encoder(string: str) -> str:
    return bytes_str_repr(string.encode("utf-8"))


def quoted_printable_encoder(string: str) -> str:
    return bytes_str_repr(quopri.encodestring(string.encode("utf-8")))


def b16_encoder(string: str) -> str:
    return bytes_str_repr(base64.b16encode(string.encode("utf-8")))


def b32_encoder(string: str) -> str:
    return bytes_str_repr(base64.b32encode(string.encode("utf-8")))


def b64_encoder(string: str) -> str:
    return bytes_str_repr(base64.b64encode(string.encode("utf-8")))


Encoder = {
    ContentEncoding.SEVEN_BIT: seven_bit_encoder,
    ContentEncoding.EIGHT_BIT: eight_bit_encoder,
    ContentEncoding.BINARY: binary_encoder,
    ContentEncoding.QUOTED_PRINTABLE: quoted_printable_encoder,
    ContentEncoding.BASE16: b16_encoder,
    ContentEncoding.BASE32: b32_encoder,
    ContentEncoding.BASE64: b64_encoder,
}


def encode(string: str, encoding: Optional[ContentEncoding]) -> str:
    return Encoder.get(encoding, lambda s: s)(string)


class String(BaseSchema):
    minLength: Optional[float] = 0
    maxLength: Optional[float] = 50
    pattern: Optional[str] = None
    format: Optional[str] = None
    # enum: Optional[List[Union[str, int, float]]] = None  # NOTE: Not used - enums go to enum class
    # contentMediaType: Optional[str] = None  # TODO: Long list, need to document which ones will be supported and how to extend
    contentEncoding: Optional[ContentEncoding]
    # contentSchema # No docs detailing this yet...

    def generate(self, context: Dict[str, Any]) -> Optional[str]:
        try:
            s = super().generate(context)
            return str(encode(s, self.contentEncoding)) if s else s
        except ProviderNotSetException:
            format_map["regex"] = lambda: rstr.xeger(self.pattern)
            format_map["relative-json-pointer"] = lambda: random.choice(
                context["state"]["__all_json_paths__"]
            )
            if format_map.get(self.format) is not None:
                return encode(format_map[self.format](), self.contentEncoding)
            if self.pattern is not None:
                return encode(rstr.xeger(self.pattern), self.contentEncoding)
            return encode(
                random_fixed_length_sentence(self.minLength, self.maxLength), self.contentEncoding
            )

    def model(self, context: Dict[str, Any]):
        return self.to_pydantic(context, str)

    def from_dict(d):
        return String(**d)
