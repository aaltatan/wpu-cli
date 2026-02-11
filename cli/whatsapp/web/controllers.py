# ruff: noqa: B008
from dataclasses import dataclass

from typer_di import Depends, TyperDI

from cli.whatsapp.options import FilepathArg
from cli.whatsapp.readers import read_messages_from_xlsx

from .options import (
    MaxMessagesTimeoutOpt,
    MaxSendSelectorTimeoutOpt,
    MinMessagesTimeoutOpt,
    MinSendSelectorTimeoutOpt,
    PageloadTimeoutOpt,
    UrlOpt,
)
from .readers import get_messages
from .schemas import Message
from .services import open_whatsapp_web_page, send_whatsapp_messages_web

app = TyperDI()


@dataclass
class Timeout:
    min_between_messages: MinMessagesTimeoutOpt
    max_between_messages: MaxMessagesTimeoutOpt
    min_send_selector: MinSendSelectorTimeoutOpt
    max_send_selector: MaxSendSelectorTimeoutOpt
    pageload: PageloadTimeoutOpt


def read_messages_from_xlsx_wrapper(filepath: FilepathArg) -> list[Message]:
    messages = read_messages_from_xlsx(filepath)
    return get_messages(messages)


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
