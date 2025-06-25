import typer
from rich.console import Console

from .controllers import get_dollar_lira_exchange_rates, get_sp_today_exchange_rates
from .schemas import DollarLiraCurrency, SpTodayExchangeRate
from .tables import dollar_lira, sp_today

app = typer.Typer()
console = Console()


@app.command(name="dollar-lira")
def dollar_lira_exchange_rates():
    """Show currencies from Syrian Exchange"""
    exchange_rates: list[DollarLiraCurrency] = get_dollar_lira_exchange_rates(
        url="https://dollar-lira.com/syrian-exchange/updates/updates.json"
    )

    for rate in exchange_rates:
        dollar_lira.add_row(*rate.to_rich_row())

    console.print(dollar_lira)


@app.command(name="sp-today")
def sp_today_exchange_rates():
    """Show currencies from Syrian Exchange"""
    exchange_rates: list[SpTodayExchangeRate] = get_sp_today_exchange_rates(
        url="https://www.sp-today.com/currencies"
    )

    for rate in exchange_rates:
        sp_today.add_row(*rate.to_rich_row())

    console.print(sp_today)
