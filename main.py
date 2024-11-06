import typer


if __name__ == "__main__":
    
    app = typer.Typer(name='edu@tech')

    # typers
    from src import vouchers, whatsapp
    
    app.add_typer(vouchers.app, name='vouchers')
    app.add_typer(whatsapp.app, name='whatsapp')
    
    app()
