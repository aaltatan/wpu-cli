# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .options import WebOptions
from .services import open_whatsapp_web_page, send_whatsapp_messages_web

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("web")
def send_whatsapp_messages_web_cmd(options: WebOptions = Depends(WebOptions)) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    with open_whatsapp_web_page(options.url, options.timeout.pageload) as page:
        send_whatsapp_messages_web(page, options.messages, options.timeout)
