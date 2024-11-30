from typing import Iterable

import typer
from rich.console import Console
from rich.table import Table

from ...models import TaxLayer

app = typer.Typer()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("#", style="blue", justify="right")
table.add_column("from", style="white", justify="right")
table.add_column("to", style="white", justify="right")
table.add_column("rate", style="white", justify="right")

console = Console()


@app.command(name="list")
def list_layers(tax_id: int = 1):
    """
    List all layers
    """
    layers: Iterable[TaxLayer] = TaxLayer.select().where(TaxLayer.tax_id == tax_id)
    for layer in layers:
        table.add_row(
            str(layer.id),
            f"{layer.from_:,}",
            f"{layer.to_:,}",
            f"{layer.rate:.2%}",
        )
    console.print(table)


@app.command()
def add():
    """
    Add a new layer
    """
    from_ = typer.prompt("From", default=0, type=int)
    to = typer.prompt("To", default=0, type=int)
    rate = typer.prompt("Rate", default=0, type=float)
    taxes_id = typer.prompt("Taxes ID", default=1, type=int)

    layer = TaxLayer.create(from_, to, rate, taxes_id)

    console.print(layer)
    console.print("Layer added successfully")


@app.command()
def update(id: int):
    """
    Update a layer
    """
    layer: TaxLayer = TaxLayer.get_by_id(id)

    from_ = typer.prompt("From", default=layer.from_, type=int)
    to = typer.prompt("To", default=layer.to_, type=int)
    rate = typer.prompt("Rate", default=layer.rate, type=float)
    taxes_id = typer.prompt("Taxes ID", default=1, type=int)

    layer.from_ = from_
    layer.to_ = to
    layer.rate = rate
    layer.tax_id = taxes_id

    layer.save()

    console.print(layer)


@app.command()
def delete(id: int):
    """
    Delete a layer
    """
    TaxLayer.delete_by_id(id)
    console.print("Layer deleted successfully")
