import json

import pytest

from ..jsf.parser import JSF
from ..jsf.schema_types import *


@pytest.mark.parametrize(
    "filestem, expected_type",
    [
        ("array", Array),
        ("boolean", Boolean),
        ("enum", Enum),
        ("inner-ref", Object),
        ("integer", Integer),
        ("null", Null),
        ("number", Number),
        ("object", Object),
        ("string-enum", Enum),
        ("string", String),
        ("tuple", Tuple),
    ],
)
def test_types(TestData, filestem, expected_type):
    with open(TestData / f"{filestem}.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, expected_type)


def test_nested_array(TestData):
    with open(TestData / f"array.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Array)
    assert hasattr(p.root, "items")
    assert isinstance(p.root.items, Enum)


def test_nested_tuple(TestData):
    with open(TestData / f"tuple.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Tuple)
    assert hasattr(p.root, "items")
    expected_types = [Number, String, String, String]
    assert [isinstance(item, expected_types[i]) for i, item in enumerate(p.root.items)]


def test_nested_object(TestData):
    with open(TestData / f"object.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {"name": String, "credit_card": Number, "test": Integer, "non_required": Integer}
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types


def test_nested_object_ref(TestData):
    with open(TestData / f"inner-ref.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {"user": Object}
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types
    expected_types = {"birthday": String, "email": String, "name": String, "id": Integer}
    assert {prop.name: type(prop) for prop in p.root.properties[0].properties} == expected_types

