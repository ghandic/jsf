import json
from pathlib import Path

from jsf.cli import app
from jsonschema import validate
from typer.testing import CliRunner

runner = CliRunner()


def test_app(TestData):
    file = Path("tmp.json")
    try:
        result = runner.invoke(
            app, ["--schema", TestData / "custom.json", "--instance", "tmp.json"]
        )
        assert result.exit_code == 0
        assert file.exists()
        with open(file, "r") as f:
            instance = json.load(f)
        with open(TestData / "custom.json", "r") as f:
            schema = json.load(f)
        validate(instance, schema)
    finally:
        file.unlink()
