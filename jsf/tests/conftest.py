from pathlib import Path

import pytest  # pants: no-infer-dep


@pytest.fixture()
def TestData():
    yield Path(__file__).parent.resolve() / "data"
