import typer

from . import desktop, web

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages."""


app.add_typer(web.app, name="web")
app.add_typer(desktop.app, name="desktop")
