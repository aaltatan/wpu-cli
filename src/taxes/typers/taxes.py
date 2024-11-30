import typer
from rich.console import Console
from rich.table import Table

from src.models import Tax as DBTax

app = typer.Typer()


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
    taxes = DBTax.select()
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
    DBTax.create(name=name, description=description)
    console.print(f"{name} tax added successfully")


@app.command()
def update(id: int):
    """
    Update a tax
    """
    tax = DBTax.get_by_id(id)

    name = typer.prompt("Name", default=tax.name)
    description = typer.prompt("Description", default=tax.description)

    tax.name = name
    tax.description = description
    tax.save()
    console.print(f"{name} tax updated successfully")


@app.command()
def delete(id: int):
    """
    Delete a tax
    """
    DBTax.delete(id=id)
    print("Layer deleted successfully")
