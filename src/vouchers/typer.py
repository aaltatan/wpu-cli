import typer

from . import controllers

from src import utils as src_utils


app = typer.Typer()
filepath = src_utils.get_salaries_filepath()


@app.command()
def add_salaries(timeout: int = 5_000, chapter: str = '1'):
    """
    add from `Journal Entry Template` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    data = controllers.get_salaries_voucher_data(filepath, chapter)
    controllers.add_voucher(timeout, data)


@app.command()
def add(
    timeout: int = 5_000, chapter: str = '1', sheet_name = 'voucher'
):
    """
    add from `voucher` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    data = controllers.get_voucher_data(filepath, chapter, sheet_name)
    controllers.add_voucher(timeout, data)