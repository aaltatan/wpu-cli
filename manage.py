import typer
from cli import edutech, fuzz, taxes, templates, whatsapp
from cli.logger import init_logger
from dotenv import load_dotenv


def callback() -> None:
    """Al-Wataniya Private University CLI."""


def main() -> None:
    load_dotenv()
    init_logger()

    app = typer.Typer(name="wpu", callback=callback)

    app.add_typer(whatsapp.app, name="whatsapp")
    app.add_typer(edutech.app, name="edutech")
    app.add_typer(taxes.app, name="tax")
    app.add_typer(templates.app, name="templates")
    app.add_typer(fuzz.app, name="fuzz")

    app()


if __name__ == "__main__":
    main()
