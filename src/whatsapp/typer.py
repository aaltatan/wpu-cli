import typer

from . import controllers

from src import utils as src_utils


typer = typer.Typer()


@typer.command()
def send(
    filename: str = "sheet1",
    extension: str = "xlsx",
    sheet_name: str = "whatsapp",
    first_cell: tuple[int, int] = (1, 1),
    last_column: int = 2,
) -> None:
    """
    send whatsapp messages from excel file.
    """
    filepath = controllers.get_filepath(filename, extension)

    has_password: bool = typer.confirm(
        'does file have a password',
        default=False
    )

    password = None
    if has_password:
        password = typer.prompt(
            "Enter password for file", hide_input=True
        )

    messages = controllers.get_messages_from_excel(
        filepath, 
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    controllers.send_messages(messages)


@typer.command()
def send_salaries(
    sheet_name: str = "whatsapp",
    first_cell: tuple[int, int] = (1, 2),
    last_column: int = 3,
):
    """
    send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    filepath = src_utils.get_salaries_filepath()
    password = typer.prompt(
        "Enter password for Salaries.xlsb file", hide_input=True
    )
    messages = controllers.get_messages_from_excel(
        filepath, 
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    controllers.send_messages(messages)