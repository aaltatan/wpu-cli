from pathlib import Path

import typer
from dotenv import load_dotenv


if __name__ == "__main__":
    
    BASE_DIR = Path().resolve(__file__)
    
    dotenv_path = BASE_DIR / '.env'
    load_dotenv(dotenv_path)
    
    app = typer.Typer(name='edu@tech')

    # typers
    from src import vouchers
    
    app.add_typer(vouchers.app, name='vouchers')
    
    app()
