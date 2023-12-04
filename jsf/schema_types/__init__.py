from typing import Union

from jsf.schema_types._tuple import JSFTuple
from jsf.schema_types.allof import AllOf
from jsf.schema_types.anyof import AnyOf
from jsf.schema_types.array import Array
from jsf.schema_types.boolean import Boolean
from jsf.schema_types.enum import JSFEnum
from jsf.schema_types.null import Null
from jsf.schema_types.number import Integer, Number
from jsf.schema_types.object import Object
from jsf.schema_types.oneof import OneOf
from jsf.schema_types.string import String

Primitives = {
    "number": Number,
    "string": String,
    "integer": Integer,
    "object": Object,
    "boolean": Boolean,
    "null": Null,
}

AllTypes = Union[
    JSFEnum,
    Object,
    Array,
    JSFTuple,
    String,
    Boolean,
    Null,
    Number,
    Integer,
    AnyOf,
    AllOf,
    OneOf,
]
PrimitiveTypes = Union[String, Boolean, Null, Number, Integer]
