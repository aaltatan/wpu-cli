import typer


if __name__ == "__main__":
    
    app = typer.Typer(name='edu@tech')

    # typers
    from src import (
        vouchers, whatsapp, taxes, salaries_calculator, central_bank_scraper
    )
    
    app.add_typer(vouchers.typer, name='vouchers')
    app.add_typer(whatsapp.typer, name='whatsapp')
    app.add_typer(taxes.taxes_typer, name='taxes')
    app.add_typer(taxes.layers_typer, name='layers')
    app.add_typer(salaries_calculator.typer, name='salaries')
    app.add_typer(central_bank_scraper.typer, name='cb')
    
    app()
