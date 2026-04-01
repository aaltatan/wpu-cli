# ruff: noqa: B008
import typer
from typer_di import Depends, TyperDI

from .dependencies import Array, WriterFn, get_calculated_data, get_writer_fn

app = TyperDI()


@app.callback(no_args_is_help=True)
def main() -> None:
    """Salaries excel (xlsb) file commands."""


@app.command(name="calc", no_args_is_help=True)
def calculate(
    data: Array[float] = Depends(get_calculated_data),
    writer_fn: WriterFn | None = Depends(get_writer_fn),
) -> None:
    """Calculate salaries in the main sheet (Data)."""
    if writer_fn:
        ws = writer_fn(data)
        typer.echo(f"Results written to {ws.name}")

    total = sum(row[-1] for row in data)
    typer.echo(f"{total = :,.2f}")
