import typer
from cli import edutech, taxes, whatsapp
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    app = typer.Typer(name="Al-Wataniya Private University CLI")

    app.add_typer(taxes.app, name="tax")
    app.add_typer(whatsapp.app, name="whatsapp")
    app.add_typer(edutech.app, name="edutech")

    app()


if __name__ == "__main__":
    main()
