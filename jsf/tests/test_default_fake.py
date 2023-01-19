import json
import re

import jwt
from jsf.parser import JSF


def test_fake_object_no_properties(TestData):
    with open(TestData / "object_no_properties.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    [p.generate() for _ in range(10)]  # Just validating no errors


def test_fake_anyof(TestData):
    with open(TestData / "anyof.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, str) or isinstance(d, float)


def test_fake_allof(TestData):
    with open(TestData / "allof.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, str) and len(d) <= 5


def test_fake_allof_complex(TestData):
    with open(TestData / "allof-complex.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, dict)
        assert set(d.keys()) == {"prometheus"}
        assert set(d["prometheus"].keys()) == {"port", "path"}
        assert isinstance(d["prometheus"]["port"], int)
        assert isinstance(d["prometheus"]["path"], str)


def test_fake_anyof_object(TestData):
    with open(TestData / "anyof_object.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, dict)
        assert ("name" in d["ob"]) or ("id" in d["ob"])


def test_fake_oneof(TestData):
    with open(TestData / "oneof.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, bool) or isinstance(d, str)


def test_fake_oneof_allof(TestData):
    with open(TestData / "oneof_allof.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, bool) or (isinstance(d, str) and len(d) <= 5)


def test_fake_oneof_object(TestData):
    with open(TestData / "oneof_object.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    fake_data = [p.generate() for _ in range(10)]
    for d in fake_data:
        assert isinstance(d, dict)
        assert ("name" in d["ob"]) or ("id" in d["ob"])


def test_fake_boolean(TestData):
    with open(TestData / "boolean.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), bool)
    fake_data = [p.generate() for _ in range(100)]
    assert False in fake_data
    assert True in fake_data


def test_fake_string(TestData):
    with open(TestData / "string.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    assert isinstance(p.generate(), str)
    fake_data = [p.generate() for _ in range(100)]
    assert len(fake_data) - len(set(fake_data)) < 50


def test_fake_string_content_encoding(TestData):
    with open(TestData / "string-content-encoding.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(100)]
    for d in fake_data:
        assert set(d["binary"]) - {"1", "0"} == set()
        # TODO: Test other encodings are working as expected


def test_fake_string_content_type(TestData):
    with open(TestData / "string-content-type.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(10)]  # Reducing for rate limiting of external requests
    for d in fake_data:
        assert len(d["text/plain"]) >= 5 and len(d["text/plain"]) <= 10

        decoded_jwt = jwt.decode(d["application/jwt"], options={"verify_signature": False})
        assert set(decoded_jwt.keys()) == {"exp", "iss"}
        assert isinstance(decoded_jwt["exp"], int)
        assert isinstance(decoded_jwt["iss"], str)


def test_fake_null(TestData):
    with open(TestData / "null.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), type(None))
    fake_data = [p.generate() for _ in range(100)]
    assert len(set(fake_data)) == 1


def test_fake_enum(TestData):
    with open(TestData / "enum.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), (str, type(None), int))
    assert all(p.generate() in ["red", "amber", "green", None, 42] for _ in range(100))


def test_fake_string_enum(TestData):
    with open(TestData / "string-enum.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), str)
    assert all(p.generate() in ["Street", "Avenue", "Boulevard"] for _ in range(100))


def test_fake_int(TestData):
    with open(TestData / "integer.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), int)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d <= 700 for d in fake_data)
    assert all(d > 600 for d in fake_data), fake_data
    assert all(d != 600 for d in fake_data)
    assert all(d % 7 == 0 for d in fake_data)


def test_fake_number(TestData):
    with open(TestData / "number.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), float)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d <= 700 for d in fake_data)
    assert all(d > 600 for d in fake_data), fake_data
    assert all(d != 600 for d in fake_data)


def test_fake_number_exclusive(TestData):
    with open(TestData / "number-exclusive.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), float)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d < 700 for d in fake_data)
    assert all(d >= 600 for d in fake_data), fake_data
    assert all(d != 700 for d in fake_data)


def test_fake_number_exclusive_float(TestData):
    with open(TestData / "number-exclusive-float.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), float)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(d < 700 for d in fake_data), fake_data
    assert all(d > 600 for d in fake_data), fake_data
    assert all(d != 700 for d in fake_data)
    assert all(d != 600 for d in fake_data)


def test_fake_array(TestData):
    with open(TestData / "array.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), list)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(set(d) - {"red", "amber", "green"} == set() for d in fake_data), fake_data
    assert all(len(set(d)) == len(d) for d in fake_data), fake_data
    assert all(len(d) <= 5 for d in fake_data), fake_data
    assert all(len(d) >= 1 for d in fake_data), fake_data


def test_fake_array_dicts(TestData):
    with open(TestData / "array-dicts.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(len(d["Basket"]) == 2 for d in fake_data), fake_data
    assert all(
        d["Basket"][0]["Item Name"] in ["A", "B", "C", "D", "E"] for d in fake_data
    ), fake_data
    assert all(
        d["Basket"][1]["Item Name"] in ["A", "B", "C", "D", "E"] for d in fake_data
    ), fake_data
    assert all(0 <= d["Basket"][0]["Amount"] < 5 for d in fake_data), fake_data
    assert all(0 <= d["Basket"][1]["Amount"] < 5 for d in fake_data), fake_data


def test_fake_array_fixed_int(TestData):
    with open(TestData / "array-fixed-int.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), list)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(set(d) - {"red", "amber", "green"} == set() for d in fake_data), fake_data
    assert all(len(d) == 5 for d in fake_data), fake_data


def test_fake_array_fixed_str(TestData):
    with open(TestData / "array-fixed-str.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), list)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(set(d) - {"red", "amber", "green"} == set() for d in fake_data), fake_data
    assert all(len(d) == 50 for d in fake_data), fake_data


def test_fake_tuple(TestData):
    with open(TestData / "tuple.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), tuple)
    fake_data = [p.generate() for _ in range(1000)]
    for d in fake_data:
        assert isinstance(d[0], float)
        assert isinstance(d[1], str)
        assert isinstance(d[2], str) and d[2] in ["Street", "Avenue", "Boulevard"]
        assert isinstance(d[3], str) and d[3] in ["NW", "NE", "SW", "SE"]


def test_fake_object(TestData):
    with open(TestData / "object.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(isinstance(d["name"], str) for d in fake_data), fake_data
    assert all(isinstance(d["credit_card"], float) for d in fake_data), fake_data
    assert all(isinstance(d["test"], int) for d in fake_data), fake_data


def test_fake_object_pattern_properties(TestData):
    with open(TestData / "object-pattern-properties.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(1000)]
    assert all(isinstance(d["name"], str) for d in fake_data), fake_data
    all_str_names = set()
    all_int_names = set()
    for d in fake_data:
        string_types = [k for k in d.keys() if k.startswith("S_")]
        int_types = [k for k in d.keys() if k.startswith("I_")]
        all_str_names = all_str_names.union(set(string_types))
        all_int_names = all_int_names.union(set(int_types))
        assert all(isinstance(d[key], str) for key in string_types)
        assert all(isinstance(d[key], int) for key in int_types)

    assert len(all_str_names) > 0
    assert len(all_int_names) > 0


def test_fake_string_format(TestData):
    with open(TestData / "string-format.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)

    assert isinstance(p.generate(), dict)
    fake_data = [p.generate() for _ in range(10)]
    assert all(bool(re.match(r".*@.*", d["email"])) for d in fake_data), fake_data
    assert all(bool(re.match(r".*@.*", d["idn-email"])) for d in fake_data), fake_data
    assert all(
        bool(re.match(r"\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}\:\d{2}\+\d{2}\:\d{2}", d["date-time"]))
        for d in fake_data
    ), fake_data
    assert all(bool(re.match(r"\d{4}-\d{2}-\d{2}", d["date"])) for d in fake_data), fake_data
    assert all(
        bool(
            re.match(
                r"^(-?)P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$",
                d["duration"],
            )
        )
        for d in fake_data
    ), fake_data
    assert all(
        bool(re.match(r"\d{2}\:\d{2}\:\d{2}\+\d{2}\:\d{2}", d["time"])) for d in fake_data
    ), fake_data
    assert all(
        bool(re.match(r"[a-zA-Z0-9+-\.]{1,33}\.[a-z]{2,4}", d["hostname"])) for d in fake_data
    )
    assert all(
        bool(re.match(r"[a-zA-Z0-9+-\.]{1,33}\.[a-z]{2,4}", d["idn-hostname"])) for d in fake_data
    )
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


# NO LONGER REQUIRED - dont think you can have unique items in a tuple?
# def test_unique_items_tuple(TestData):
#     with open(TestData / "unique-items-tuple.json", "r") as file:
#         schema = json.load(file)
#     p = JSF(schema)
#     fake_data = p.generate(50)
#     for f in fake_data:
#         assert isinstance(f, list)
#         assert all([isinstance(t, tuple) for t in f])
#         assert all(len(set(t)) == len(t) for t in f), f


def test_unique_items_array(TestData):
    with open(TestData / "unique-items-array.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    fake_data = p.generate(50)
    for f in fake_data:
        assert isinstance(f, list)
        assert all([isinstance(t, bool) for t in f])
        assert len(set(f)) == len(f), f


def test_const(TestData):
    with open(TestData / "const.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    fake_data = p.generate(50)
    for f in fake_data:
        assert isinstance(f, dict)
        assert isinstance(f["country"], str)
        assert f["country"] == "United States of America"


def test_external_ref(TestData):
    with open(TestData / "external-ref.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    fake_data = p.generate(50)
    for f in fake_data:
        assert isinstance(f, dict)
        assert isinstance(f["ReferenceToLocalSchema"], dict)
        assert isinstance(f["ReferenceToLocalSchema"]["no-write"], bool)

        assert isinstance(f["ReferenceToExternalSchema"], dict)
        assert isinstance(f["ReferenceToExternalSchema"]["src"], list)
        assert all(isinstance(t, str) for t in f["ReferenceToExternalSchema"]["src"])


def test_gen_and_validate(TestData):
    with open(TestData / "custom.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    [p.generate_and_validate() for _ in range(50)]


def test_list_of_types(TestData):
    with open(TestData / "type-list.json", "r") as file:
        schema = json.load(file)
    fake_data = [JSF(schema).generate() for _ in range(100)]
    for f in fake_data:
        print(f)
    assert all(isinstance(f, dict) for f in fake_data), fake_data
    assert all(type(f["randTypeValueNullable"]) in [type(None), bool] for f in fake_data), fake_data
    assert all(type(f["randTypeValue"]) in [bool, int, float, str] for f in fake_data), fake_data
    assert all(isinstance(f["int"], int) for f in fake_data), fake_data
    assert all(isinstance(f["null"], type(None)) for f in fake_data), fake_data
