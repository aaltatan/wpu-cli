import typer
from rich.console import Console
from rich.table import Table

from .controllers import get_currencies
from .schemas import Currency

app = typer.Typer()

console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Pre-Buy", style="bold")
table.add_column("Pre-Sell", style="bold")
table.add_column("Buy", style="bold")
table.add_column("Sell", style="bold")
table.add_column("Change", style="bold")
table.add_column("Updated At", style="bold")
table.add_column("Title", style="bold")


@app.command(name="list")
def currencies():
    """ Show currencies from Syrian Exchange """
    currencies: list[Currency] = get_currencies()

    for currency in currencies:
        table.add_row(*currency.to_rich_table())

    console.print(table)