import typer
from rich.console import Console
from rich.table import Table

from src.db import Database, NotFoundError

from ..schemas import Tax

app = typer.Typer()

db = Database()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("#", style="blue", justify="right")
table.add_column("name", style="white", justify="right")
table.add_column("description", style="white", justify="right")

console = Console()


@app.command(name="list")
def list_taxes():
    """
    List all taxes
    """
    taxes = db.get_taxes()
    for tax in taxes:
        table.add_row(
            str(tax.id),
            tax.name,
            tax.description,
        )
    console.print(table)


@app.command()
def add():
    """
    Add a new tax
    """
    name = typer.prompt("Name", default="Syrian Layers Tax")
    description = typer.prompt("Description", default="Default taxes")
    db.add_tax(Tax(name, description))
    console.print(f"{name} tax added successfully")


@app.command()
def update(id: int):
    """
    Update a tax
    """
    try:
        tax = db.get_tax(id)
    except NotFoundError:
        console.print("Tax not found")
        return

    name = typer.prompt("Name", default=tax.name)
    description = typer.prompt("Description", default=tax.description)
    db.update_tax(id, Tax(name, description))
    console.print(f"{name} tax updated successfully")


@app.command()
def delete(id: int):
    """
    Delete a tax
    """
    db.delete_layer(id)
    print("Layer deleted successfully")
