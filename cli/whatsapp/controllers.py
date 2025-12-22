# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .options import Options
from .services import open_whatsapp_page, send_whatsapp_messages

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages_cmd(options: Options = Depends(Options)) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    with open_whatsapp_page(options.url, options.timeout.pageload) as page:
        send_whatsapp_messages(page, options.messages, options.timeout)
