import typer

from .controllers import main


app = typer.Typer()


@app.command()
def add_from_excel(timeout: int = 5_000, chapter: str = '1'):
    """
    add from JOURNAL_ENTRY sheet in Salaries_Wages_202***.xlsb file
    """
    main(timeout, chapter)

