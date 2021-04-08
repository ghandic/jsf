from typing import Union

from .array import Array
from .number import Number, Integer
from .object import Object
from .string import String
from ._tuple import Tuple
from .enum import Enum
from .null import Null
from .boolean import Boolean

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
