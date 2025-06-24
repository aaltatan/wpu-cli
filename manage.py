import typer

if __name__ == "__main__":
    app = typer.Typer(name="edu@tech")

    # typers
    from src import (
        capacity_calculator,
        central_bank_scraper,
        salaries_calculator,
        syrian_exchange_scraper,
        taxes,
        vouchers,
        whatsapp,
    )

    app.add_typer(salaries_calculator.app, name="salaries")
    app.add_typer(central_bank_scraper.app, name="cb")
    app.add_typer(syrian_exchange_scraper.app, name="bm")
    app.add_typer(vouchers.app, name="vouchers")
    app.add_typer(whatsapp.app, name="whatsapp")
    app.add_typer(taxes.taxes_app, name="taxes")
    app.add_typer(taxes.layers_app, name="layers")
    app.add_typer(capacity_calculator.app, name="capacity")

    app()
