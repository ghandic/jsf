from pathlib import Path

import typer  # pants: no-infer-dep

from jsf.parser import JSF

app = typer.Typer()


@app.command()
def main(
    schema: Path = typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    instance: Path = typer.Option(
        ...,
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
    ),
):
    JSF.from_json(schema).to_json(instance)
