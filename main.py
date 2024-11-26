import typer


if __name__ == "__main__":
    
    app = typer.Typer(name='edu@tech')

    # typers
    from src import vouchers, whatsapp, taxes
    
    app.add_typer(vouchers.typer, name='vouchers')
    app.add_typer(whatsapp.typer, name='whatsapp')
    app.add_typer(taxes.taxes_typer, name='taxes')
    app.add_typer(taxes.layers_typer, name='layers')
    
    app()
