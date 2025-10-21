import typer
from typing_extensions import Annotated

from cli.utils import get_salaries_filepath

from .services import get_messages_from_excel, send_messages

app = typer.Typer()


@app.command()
def send_salaries(
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="Password for Salaries.xlsb file",
            hide_input=True,
            prompt=True,
            envvar="EXCEL_FILE_PASSWORD",
        ),
    ],
    sheet_name: Annotated[
        str,
        typer.Option("--sheet", "-s", help="Sheet name in Salaries.xlsb file"),
    ] = "whatsapp",
    first_cell: Annotated[
        tuple[int, int],
        typer.Option("--first-cell", "-f", help="Start cell in Salaries.xlsb file"),
    ] = (1, 2),
    last_column: Annotated[
        int,
        typer.Option("--last-column", "-l", help="Last column in Salaries.xlsb file"),
    ] = 3,
):
    """
    send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    filepath = get_salaries_filepath()
    messages = get_messages_from_excel(
        filepath,
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    send_messages(messages)
