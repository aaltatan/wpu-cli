import typer
from syriantaxes import calculate_brackets_tax

from .callbacks import app_callback

app = typer.Typer(callback=app_callback)


@app.command(name="brackets")
def calculate_brackets_tax_command(
    ctx: typer.Context,
):
    pass
