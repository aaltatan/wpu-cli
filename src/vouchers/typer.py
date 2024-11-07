import typer

from . import controllers

from src import utils as src_utils


typer = typer.Typer()
filepath = src_utils.get_salaries_filepath()


@typer.command()
def add_salaries(
    timeout: int = 5_000, 
    chapter: str = '1', 
    start_cell: tuple[int, int] = (1, 2),
    last_column: int = 7,
    sheet_name: str = 'Journal Entry Template',
):
    """
    add from `Journal Entry Template` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    username: str = typer.prompt(
        "Enter username for Automata", default='abdullah.tatan'
    )
    password: str = typer.prompt(
        "Enter password for Automata", hide_input=True
    )
    excel_password: str = typer.prompt(
        "Enter password for excel file", hide_input=True
    )
    data = controllers.get_salaries_voucher_data(
        filepath, 
        password=excel_password, 
        chapter=chapter,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )
    controllers.add_voucher(
        timeout, data, username=username, password=password
    )


@typer.command()
def add(
    timeout: int = 5_000, chapter: str = '1', sheet_name = 'voucher'
):
    """
    add from `voucher` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    username: str = typer.prompt("Enter username for Automata")
    password: str = typer.prompt(
        "Enter password for Automata", hide_input=True
    )
    excel_password: str = typer.prompt(
        "Enter password for excel file", hide_input=True
    )
    data = controllers.get_voucher_data(
        filepath, chapter, sheet_name, password=excel_password
    )
    controllers.add_voucher(
        timeout, data, username=username, password=password
    )