import json

from jsf.parser import JSF


def test_string_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["str"])

    actual = [p.generate() for _ in range(100)]
    assert all(each not in ["None"] for each in actual)
    assert all(type(each) in [type(None), str] for each in actual)


def test_int_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["int"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each) in [type(None), int] for each in actual)


def test_number_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["num"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each) in [type(None), float] for each in actual)


def test_boolean_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["bool"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each) in [type(None), bool] for each in actual)


def test_enum_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["enum"])

    actual = [p.generate() for _ in range(100)]
    assert all(each in ["r", "g", "b", None] for each in actual)


def test_array_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["arr"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each) in [list, type(None)] for each in actual)


def test_array_nested_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["arr_nested"])

    actual = [p.generate() for _ in range(100)]
    items = [item for each in actual for item in each]

    assert all(type(each) in [int, type(None)] for each in items)


def test_object_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["obj"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each) in [dict, type(None)] for each in actual)


def test_object_nested_null_gen(TestData):
    with open(TestData / "type-list-null.json") as file:
        schema = json.load(file)
    p = JSF(schema["obj_nested"])

    actual = [p.generate() for _ in range(100)]
    assert all(type(each["req"]) in [bool, type(None)] for each in actual)
