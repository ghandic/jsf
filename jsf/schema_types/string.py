import logging
import random
import re
from datetime import timezone
from typing import Any, Callable, Dict, Optional, Tuple, Type

import rstr
from faker import Faker

from jsf.schema_types.base import BaseSchema, ProviderNotSetException
from jsf.schema_types.string_utils import content_encoding, content_type
from jsf.schema_types.string_utils.content_type.text__plain import random_fixed_length_sentence

logger = logging.getLogger()
faker = Faker()

FRAGMENT = "[a-zA-Z][a-zA-Z0-9+-.]*"
URI_PATTERN = f"https?://{{hostname}}(?:{FRAGMENT})+"
PARAM_PATTERN = "(?:\\?([a-z]{1,7}(=\\w{1,5})?&){0,3})?"


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
        remainder = "".join(str(part) for part in [milliseconds, microseconds, nanoseconds] if part)
        if remainder:
            seconds = f"{seconds}.{remainder}"
        duration = f"{duration}{seconds}S"

    # Case where there was no duration specified, still need to output valid format string
    if duration == "P":
        duration = "PT0S"

    # direction
    if not positive:
        duration = f"-{duration}"

    return duration


def mostly_zero_randint(_min: int, _max: int) -> int:
    return 0 if random.random() > 0.8 else random.randint(int(_min), int(_max))


def fake_duration() -> str:
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


class String(BaseSchema):
    minLength: Optional[int] = 0
    maxLength: Optional[int] = 50
    pattern: Optional[str] = None
    format: Optional[str] = None
    # enum: Optional[List[Union[str, int, float]]] = None  # NOTE: Not used - enums go to enum class
    contentMediaType: Optional[str] = None
    contentEncoding: Optional[content_encoding.ContentEncoding] = None
    # contentSchema # Doesnt help with generation

    def generate(self, context: Dict[str, Any]) -> Optional[str]:
        try:
            s = super().generate(context)
            return str(content_encoding.encode(s, self.contentEncoding)) if s else s
        except ProviderNotSetException:
            format_map["regex"] = lambda: rstr.xeger(self.pattern)
            format_map["relative-json-pointer"] = lambda: random.choice(
                context["state"]["__all_json_paths__"]
            )
            if format_map.get(self.format) is not None:
                return content_encoding.encode(format_map[self.format](), self.contentEncoding)
            if self.pattern is not None:
                return content_encoding.encode(rstr.xeger(self.pattern), self.contentEncoding)
            if self.contentMediaType is not None:
                return content_encoding.encode(
                    content_type.generate(self.contentMediaType, self.minLength, self.maxLength),
                    self.contentEncoding,
                )
            return content_encoding.encode(
                random_fixed_length_sentence(self.minLength, self.maxLength), self.contentEncoding
            )

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        return self.to_pydantic(context, str)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "String":
        return String(**d)
