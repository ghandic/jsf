from typing import Union

from ._tuple import JSFTuple
from .array import Array
from .boolean import Boolean
from .enum import JSFEnum
from .null import Null
from .number import Integer, Number
from .object import Object
from .string import String
from .anyof import AnyOf
from .oneof import OneOf

Primitives = {
    "number": Number,
    "string": String,
    "integer": Integer,
    "object": Object,
    "boolean": Boolean,
    "null": Null,
}

AllTypes = Union[JSFEnum, Object, Array, JSFTuple, String, Boolean, Null, Number, Integer, AnyOf, OneOf]
PrimativeTypes = Union[String, Boolean, Null, Number, Integer]
