import json
import platform
from enum import Enum
from typing import List

import pytest  # pants: no-infer-dep
from jsf.parser import JSF
from pydantic.main import create_model

Object = create_model("Object")

expected = [
    ("boolean", bool),
    ("enum", Enum),
    ("inner-ref", Object),
    ("integer", int),
    ("null", type(None)),
    ("number", float),
    ("object", Object),
    ("custom", Object),
    ("string-enum", Enum),
    ("string", str),
    ("tuple", tuple),
]
if int(platform.python_version_tuple()[1]) < 9:
    expected.append(("array", List))

else:
    from typing import _GenericAlias

    def test_gen_model_list(TestData):
        with open(TestData / "array.json", "r") as file:
            schema = json.load(file)
        p = JSF(schema)
        Model = p.pydantic()
        assert _GenericAlias == type(Model)


@pytest.mark.parametrize(
    "filestem, expected_type_anno",
    expected,
)
def test_gen_model(TestData, filestem, expected_type_anno):
    with open(TestData / f"{filestem}.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    Model = p.pydantic()
    assert type(expected_type_anno) == type(Model)
