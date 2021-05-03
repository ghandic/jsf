import json
from enum import Enum
from typing import List

import pytest
from pydantic.main import create_model

from ..jsf.parser import JSF

Object = create_model("Object")


@pytest.mark.parametrize(
    "filestem, expected_type_anno",
    [
        ("array", List),
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
    ],
)
def test_gen_model(TestData, filestem, expected_type_anno):
    with open(TestData / f"{filestem}.json", "r") as file:
        schema = json.load(file)
    p = JSF(schema)
    Model = p.pydantic()
    print(type(Model))
    assert type(expected_type_anno) == type(Model)
