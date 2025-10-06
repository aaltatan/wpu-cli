import asyncio

import typer

from src import utils as src_utils

from . import controllers

app = typer.Typer()


@app.command()
def send_salaries(
    sheet_name: str = "whatsapp",
    first_cell: tuple[int, int] = (1, 2),
    last_column: int = 3,
    method: str = "sync",
):
    """
    send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    filepath = src_utils.get_salaries_filepath()
    password = typer.prompt("Enter password for Salaries.xlsb file", hide_input=True)
    messages = controllers.get_messages_from_excel(
        filepath,
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    if method == "sync":
        controllers.send_messages_sync(messages)
    else:
        asyncio.run(controllers.send_messages_async(messages))
