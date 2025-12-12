from typer import Typer

from . import reports, vouchers

app = Typer()


@app.callback()
def main():
    """Make automated tasks in Automota@Edutech app."""


app.add_typer(reports.app, name="reports")
app.add_typer(vouchers.app, name="vouchers")
