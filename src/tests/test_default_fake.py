import json
import re

from ..jsf.parser import JSF


def test_fake_boolean(TestData):
    with open(TestData / f"boolean.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), bool)
    fake_data = [p.generate() for _ in range(100)]
    assert False in fake_data
    assert True in fake_data


def test_fake_string(TestData):
    with open(TestData / f"string.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), str)
    fake_data = [p.generate() for _ in range(100)]
    assert len(fake_data) - len(set(fake_data)) < 50


def test_fake_null(TestData):
    with open(TestData / f"null.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), type(None))
    fake_data = [p.generate() for _ in range(100)]
    assert len(set(fake_data)) == 1


def test_fake_enum(TestData):
    with open(TestData / f"enum.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), (str, type(None), int))
    assert all(p.generate() in ["red", "amber", "green", None, 42] for _ in range(100))


def test_fake_string_enum(TestData):
    with open(TestData / f"string-enum.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), str)
    assert all(p.generate() in ["Street", "Avenue", "Boulevard"] for _ in range(100))


def test_fake_int(TestData):
    with open(TestData / f"integer.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), int)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d <= 700 for d in fake_data)
    assert all(d > 600 for d in fake_data), fake_data
    assert all(d != 600 for d in fake_data)
    assert all(d % 7 == 0 for d in fake_data)


def test_fake_number(TestData):
    with open(TestData / f"number.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), float)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d <= 700 for d in fake_data)
    assert all(d > 600 for d in fake_data), fake_data
    assert all(d != 600 for d in fake_data)


def test_fake_array(TestData):
    with open(TestData / f"array.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), list)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(set(d) - {"red", "amber", "green", None, 42} == set() for d in fake_data), fake_data
    assert all(len(set(d)) == len(d) for d in fake_data), fake_data
    assert all(len(d) <= 5 for d in fake_data), fake_data
    assert all(len(d) >= 1 for d in fake_data), fake_data


def test_fake_tuple(TestData):
    with open(TestData / f"tuple.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert all([isinstance(f, tuple) for f in p.generate()])
    fake_data = [p.generate() for _ in range(1000)]
    for fd in fake_data:
        assert all(isinstance(d[0], float) for d in fd), fd
        assert all(isinstance(d[1], str) for d in fd), fd
        assert all(isinstance(d[2], str) and d[2] in ["Street", "Avenue", "Boulevard"] for d in fd), fd
        assert all(isinstance(d[3], str) and d[3] in ["NW", "NE", "SW", "SE"] for d in fd), fd


def test_fake_object(TestData):
    with open(TestData / f"object.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(isinstance(d["name"], str) for d in fake_data), fake_data
    assert all(isinstance(d["credit_card"], float) for d in fake_data), fake_data
    assert all(isinstance(d["test"], int) for d in fake_data), fake_data


def test_fake_string_format(TestData):
    with open(TestData / f"string-format.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(10)]
    assert all(bool(re.match(r".*@.*", d["email"])) for d in fake_data), fake_data
    assert all(bool(re.match(r".*@.*", d["idn-email"])) for d in fake_data), fake_data
    assert all(
        bool(re.match(r"\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}\:\d{2}\+\d{2}\:\d{2}", d["date-time"])) for d in fake_data
    ), fake_data
    assert all(bool(re.match(r"\d{4}-\d{2}-\d{2}", d["date"])) for d in fake_data), fake_data
    assert all(bool(re.match(r"\d{2}\:\d{2}\:\d{2}\+\d{2}\:\d{2}", d["time"])) for d in fake_data), fake_data
    assert all(bool(re.match(r"[a-zA-Z0-9+-\.]{1,33}\.[a-z]{2,4}", d["hostname"])) for d in fake_data)
    assert all(bool(re.match(r"[a-zA-Z0-9+-\.]{1,33}\.[a-z]{2,4}", d["idn-hostname"])) for d in fake_data)
    assert all(bool(re.match(r"[a-f0-9]{0,4}(:[a-f0-9]{0,4}){7}", d["ipv6"])) for d in fake_data), [
        d["ipv6"] for d in fake_data
    ]

    # TODO:  add more regex tests
    # "ipv4"
    # "uri"
    # "uri-reference"
    # "iri"
    # "iri-reference"
    # "uri-template"
    # "json-pointer"
    # "relative-json-pointer"
    # "uuid"
    # "regex"
