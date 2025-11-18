from typer import Typer

from . import reports, vouchers

app = Typer()

app.add_typer(reports.app, name="reports")
app.add_typer(vouchers.app, name="vouchers")
