import json

import pytest  # pants: no-infer-dep
from jsf.parser import JSF

from jsf.schema_types import (
    Array,
    Boolean,
    Integer,
    JSFEnum,
    JSFTuple,
    Null,
    Number,
    Object,
    String,
)


@pytest.mark.parametrize(
    "filestem, expected_type",
    [
        ("array", Array),
        ("boolean", Boolean),
        ("enum", JSFEnum),
        ("inner-ref", Object),
        ("integer", Integer),
        ("null", Null),
        ("number", Number),
        ("object", Object),
        ("string-enum", JSFEnum),
        ("string", String),
        ("tuple", JSFTuple),
    ],
)
def test_types(TestData, filestem, expected_type):
    with open(TestData / f"{filestem}.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, expected_type)


def test_nested_array(TestData):
    with open(TestData / "array.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Array)
    assert hasattr(p.root, "items")
    assert isinstance(p.root.items, JSFEnum)


def test_nested_tuple(TestData):
    with open(TestData / "tuple.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, JSFTuple)
    assert hasattr(p.root, "items")
    expected_types = [Number, String, String, String]
    assert [isinstance(item, expected_types[i]) for i, item in enumerate(p.root.items)]


def test_nested_object(TestData):
    with open(TestData / "object.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {
        "name": String,
        "credit_card": Number,
        "test": Integer,
        "non_required": Integer,
    }
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types


def test_nested_object_ref(TestData):
    with open(TestData / "inner-ref.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {"user": Object}
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types
    expected_types = {
        "birthday": String,
        "email": String,
        "name": String,
        "id": Integer,
        "uuid": String,
    }
    assert {prop.name: type(prop) for prop in p.root.properties[0].properties} == expected_types


def test_ordered_refs_object(TestData):
    with open(TestData / "ordered-refs.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {"foobar": Object}
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types
    expected_types = {
        "bar": JSFEnum,
    }
    assert {prop.name: type(prop) for prop in p.root.properties[0].properties} == expected_types


def test_unordered_refs_object(TestData):
    with open(TestData / "unordered-refs.json") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.root, Object)
    assert hasattr(p.root, "properties")
    expected_types = {"foobar": Object}
    assert {prop.name: type(prop) for prop in p.root.properties} == expected_types
    expected_types = {
        "bar": JSFEnum,
    }
    assert {prop.name: type(prop) for prop in p.root.properties[0].properties} == expected_types
