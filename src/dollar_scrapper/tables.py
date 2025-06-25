import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()

console = Console()

dollar_lira = Table(show_header=True, header_style="bold magenta")
dollar_lira.add_column("Pre-Buy", style="bold")
dollar_lira.add_column("Pre-Sell", style="bold")
dollar_lira.add_column("Buy", style="bold")
dollar_lira.add_column("Sell", style="bold")
dollar_lira.add_column("Change", style="bold")
dollar_lira.add_column("Updated At", style="bold")
dollar_lira.add_column("Title", style="bold")

sp_today = Table(show_header=True, header_style="bold magenta")
sp_today.add_column("currency", style="bold")
sp_today.add_column("currency symbol", style="bold")
sp_today.add_column("purchase", style="bold")
sp_today.add_column("sale", style="bold")

cb = Table(show_header=True, header_style="bold magenta")
cb.add_column("date", style="white", justify="right")
cb.add_column("rate", style="white", justify="right")
