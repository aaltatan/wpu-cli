import typer

from src import (
    capacity_calculator,
    dollar_scrapper,
    salaries_calculator,
    taxes,
    vouchers,
    whatsapp,
)

if __name__ == "__main__":
    app = typer.Typer(name="edu@tech")

    app.add_typer(salaries_calculator.app, name="salaries")
    app.add_typer(dollar_scrapper.app, name="dollar")
    app.add_typer(vouchers.app, name="vouchers")
    app.add_typer(whatsapp.app, name="whatsapp")
    app.add_typer(taxes.taxes_app, name="taxes")
    app.add_typer(taxes.layers_app, name="layers")
    app.add_typer(capacity_calculator.app, name="capacity")

    app()
