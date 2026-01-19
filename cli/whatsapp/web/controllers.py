# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .options import Timeout, UrlOpt, read_messages_from_xlsx_wrapper
from .schemas import Message
from .services import open_whatsapp_web_page, send_whatsapp_messages_web

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_whatsapp_messages_web_cmd(
    url: UrlOpt,
    timeout: Timeout = Depends(Timeout),
    messages: list[Message] = Depends(read_messages_from_xlsx_wrapper),
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    with open_whatsapp_web_page(url, timeout.pageload) as page:
        send_whatsapp_messages_web(page, messages, timeout)
