from copy import deepcopy

import pytest  # pants: no-infer-dep
from jsf.parser import JSF
from jsf.schema_types.string import random_fixed_length_sentence


@pytest.mark.parametrize(
    "_min, _max",
    [(0, 1), (0, 0), (0, 10), (10, 20), (10, 2000)],
)
def test_random_fixed_length_sentence(_min, _max):
    gen = random_fixed_length_sentence(_min, _max)
    assert len(gen) <= _max
    assert len(gen) >= _min


def test_base_state_deepcopy():
    p = JSF({})
    assert next(p.base_state["__counter__"]) == 1
    copied_base_state = deepcopy(p.base_state)
    assert next(copied_base_state["__counter__"]) == 2
    assert next(p.base_state["__counter__"]) == 2
