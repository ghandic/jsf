from typing import Union

from ._tuple import Tuple
from .array import Array
from .boolean import Boolean
from .enum import Enum
from .null import Null
from .number import Integer, Number
from .object import Object
from .string import String

Primitives = {
    "number": Number,
    "string": String,
    "integer": Integer,
    "object": Object,
    "boolean": Boolean,
    "null": Null,
}

AllTypes = Union[Enum, Object, Array, Tuple, String, Boolean, Null, Number, Integer]
PrimativeTypes = Union[String, Boolean, Null, Number, Integer]
