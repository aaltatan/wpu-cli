# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .options import MessagesArg, Timeout, UrlOpt
from .services import open_whatsapp_page, send_whatsapp_messages

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages_cmd(
    url: UrlOpt, messages: MessagesArg, timeout: Timeout = Depends(Timeout)
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    with open_whatsapp_page(url, timeout.pageload) as page:
        send_whatsapp_messages(page, messages, timeout)
