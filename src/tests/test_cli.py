import json
from pathlib import Path

from typer.testing import CliRunner
from jsonschema import validate

from ..jsf.cli import app

runner = CliRunner()


def test_app(TestData):
    try:
        result = runner.invoke(app, ["--schema", TestData / "custom.json", "--instance", "tmp.json"])
        assert result.exit_code == 0
        file = Path("tmp.json")
        assert file.exists()
        with open(file, "r") as f:
            instance = json.load(f)
        with open(TestData / "custom.json", "r") as f:
            schema = json.load(f)
        validate(instance, schema)
    finally:
        file.unlink()
