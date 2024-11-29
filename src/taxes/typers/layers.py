import typer
from rich.console import Console
from rich.table import Table

from src.db import Database, NotFoundError

from ..schemas import Layer

app = typer.Typer()

db = Database()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("#", style="blue", justify="right")
table.add_column("from", style="white", justify="right")
table.add_column("to", style="white", justify="right")
table.add_column("rate", style="white", justify="right")
table.add_column("tax name", style="white", justify="right")

console = Console()


@app.command(name="list")
def list_layers(tax_id: int = 1):
    """
    List all layers
    """
    layers = db.get_layers(tax_id)
    for layer in layers:
        table.add_row(
            str(layer.id),
            f"{layer.from_:,}",
            f"{layer.to_:,}",
            f"{layer.rate:.2%}",
            layer.tax_name,
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

    layer = Layer(from_, to, rate, taxes_id)

    db.add_layer(layer, taxes_id)

    console.print(layer)
    console.print("Layer added successfully")


@app.command()
def update(id: int):
    """
    Update a layer
    """

    try:
        layer = db.get_layer(id)
    except NotFoundError:
        console.print("Layer not found")
        return

    from_ = typer.prompt("From", default=layer.from_, type=int)
    to = typer.prompt("To", default=layer.to_, type=int)
    rate = typer.prompt("Rate", default=layer.rate, type=float)
    taxes_id = typer.prompt("Taxes ID", default=1, type=int)

    layer = Layer(from_, to, rate, taxes_id)

    db.update_layer(id, layer)

    console.print(layer)


@app.command()
def delete(id: int):
    """
    Delete a layer
    """
    db.delete_layer(id)
    console.print("Layer deleted successfully")
