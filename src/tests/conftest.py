from pathlib import Path

import pytest


@pytest.fixture()
def TestData():
    yield Path(__file__).parent.resolve() / "data"
