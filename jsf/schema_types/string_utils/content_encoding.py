import base64
import quopri
from enum import Enum


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


def encode(string: str, encoding: ContentEncoding) -> str:
    return Encoder.get(encoding, lambda s: s)(string)
