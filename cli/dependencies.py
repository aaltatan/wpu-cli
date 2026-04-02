from typing import Annotated

from rich.console import Console
from typer_di import Depends


def get_console() -> Console:
    return Console()


ConsoleDep = Annotated[Console, Depends(get_console)]
