import typer

from . import controllers

from src import utils as src_utils


app = typer.Typer()
filepath = src_utils.get_salaries_filepath()


@app.command()
def send_salaries():
    """
    send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file
    """
    messages = controllers.get_messages_from_excel_file(filepath)
    controllers.send_messages(messages)