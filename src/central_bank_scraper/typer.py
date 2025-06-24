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
def scrape(pages: int = 1, source: str = "transfers"):
    """
    Scrape central bank data
    """
    urls: dict[str, str] = {
        "transfers": "https://cb.gov.sy/index.php?Last=3427&CurrentPage={}&First=0&page=list&ex=2&dir=exchangerate&lang=1&service=2&sorc=0&lt=0&act=1206",
        "official": "https://cb.gov.sy/index.php?Last=3427&CurrentPage={}&First=0&page=list&ex=2&dir=exchangerate&lang=1&service=4&sorc=0&lt=0&act=1207",
    }
    url: str = urls.get(source, "transfers")

    exchange_rates: list[ExchangeRate] = asyncio.run(
        get_exchange_rates(url=url, pages=pages)
    )

    for rate in exchange_rates:
        table.add_row(*rate.to_rich_row())

    console.print(table)
