import typer
from cli import edutech, fuzz, salaries, templates, whatsapp
from cli.logger import init_logger
from dotenv import load_dotenv


def callback() -> None:
    """Al-Wataniya Private University CLI."""


def main() -> None:
    load_dotenv()
    init_logger()

    app = typer.Typer(name="wpu", callback=callback, no_args_is_help=True)

    app.add_typer(whatsapp.app, name="whatsapp")
    app.add_typer(edutech.app, name="edutech")
    app.add_typer(templates.app, name="templates")
    app.add_typer(fuzz.app, name="fuzz")
    app.add_typer(salaries.app, name="salaries")

    app()


if __name__ == "__main__":
    main()
