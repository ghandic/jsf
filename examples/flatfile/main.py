import json
from enum import Enum
from pathlib import Path

import jsonlines
import pandas as pd
import typer
from typing_extensions import Annotated

from jsf import JSF


class OutputFormat(str, Enum):
    csv = "csv"
    excel = "excel"
    parquet = "parquet"
    json = "json"
    jsonl = "jsonl"


def main(
    schema: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="Path to the JSON schema used to produce the fake data.",
        ),
    ],
    records: Annotated[int, typer.Option(min=0, help="Number of records you wish to produce.")],
    output_format: Annotated[OutputFormat, typer.Option(help="Fake data output format.")],
    output: Annotated[Path, typer.Option(help="Output file path")],
):
    faker = JSF.from_json(schema)
    fake_data = faker.generate(records)
    match output_format:
        case OutputFormat.csv:
            pd.DataFrame.from_records(fake_data).to_csv(output, index=False)
        case OutputFormat.excel:
            more_fake_data = faker.generate(records)
            custom_header = [
                v.get("title") or k for k, v in faker.root_schema["properties"].items()
            ]
            with pd.ExcelWriter(output) as excel_writer:
                pd.DataFrame.from_records(fake_data).to_excel(
                    excel_writer, sheet_name="Fake Data", index=False, header=custom_header
                )
                pd.DataFrame.from_records(more_fake_data).to_excel(
                    excel_writer, sheet_name="More Fake Data", index=False, header=custom_header
                )
        case OutputFormat.json:
            with open(output, "w") as f:
                json.dump(fake_data, f)
        case OutputFormat.jsonl:
            with jsonlines.open(output, mode="w") as writer:
                writer.write_all(fake_data)
        case OutputFormat.parquet:
            pd.DataFrame.from_records(fake_data).to_parquet(output, index=False)
        case _:
            raise NotImplementedError("Unable to produce in this file format yet")


if __name__ == "__main__":
    typer.run(main)
