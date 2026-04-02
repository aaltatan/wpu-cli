# ruff: noqa: B008
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer_di import Depends, TyperDI

from cli.dependencies import ConsoleDep

from .dependencies import Array, WriterFn, get_calculated_array, get_writer_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Salaries excel (xlsb) file commands."""


@app.command(name="calc")
def calculate(
    console: ConsoleDep,
    data: Array[float] = Depends(get_calculated_array),
    writer_fn: WriterFn | None = Depends(get_writer_fn),
) -> None:
    """Calculate salaries in the main sheet (Data)."""
    if writer_fn:
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
        ) as progress:
            progress.add_task("Writing ... ", total=None)
            ws = writer_fn(data)
            console.print("[green]Done! 👍[/green]")
            console.print(
                f'Results have been written to "{ws.name}" sheet in "{ws.book.name}" workbook.'
            )

    total = sum(row[-1] for row in data)
    console.print(f"[green]{total = :,.2f}[/green]")
