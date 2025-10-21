import typer
from dotenv import load_dotenv

from cli import taxes, vouchers, whatsapp

if __name__ == "__main__":
    load_dotenv()

    app = typer.Typer(name="Al-Wataniya Private University CLI")

    app.add_typer(taxes.app, name="taxes")
    app.add_typer(vouchers.app, name="vouchers")
    app.add_typer(whatsapp.app, name="whatsapp")

    app()
