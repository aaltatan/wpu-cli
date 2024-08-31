from pathlib import Path

import typer
from dotenv import load_dotenv

from src.vouchers.typer import app as journal_entry_app


if __name__ == "__main__":
    
    BASE_DIR = Path().resolve(__file__)
    
    dotenv_file = BASE_DIR / '.env'
    load_dotenv(dotenv_file)
    
    app = typer.Typer(name='edu@tech')

    # typers
    app.add_typer(journal_entry_app, name='vouchers')
    
    app()
