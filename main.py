import typer


if __name__ == "__main__":
    
    app = typer.Typer(name='edu@tech')

    # typers
    from src import vouchers, whatsapp
    
    app.add_typer(vouchers.typer, name='vouchers')
    app.add_typer(whatsapp.typer, name='whatsapp')
    
    app()
