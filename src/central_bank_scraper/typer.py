import asyncio

import typer
from rich.console import Console
from rich.table import Table

from .controllers import get_exchange_rates, ExchangeRate

app = typer.Typer()
console = Console()
table = Table(show_header=True, header_style="bold magenta")

table.add_column("date", style="white", justify="right")
table.add_column("rate", style="white", justify="right")


@app.command(name="list")
def scrape(pages: int = 1):
    """
    Scrape central bank data
    """
    exchange_rates: list[ExchangeRate] = asyncio.run(get_exchange_rates(pages))
    for rate in exchange_rates:
        table.add_row(*rate.to_rich_row())

    console.print(table)
