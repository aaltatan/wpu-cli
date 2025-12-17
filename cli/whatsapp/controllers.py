import typer

from .loaders import get_messages_from_xlsx
from .options import (
    FilepathArgument,
    MessagesTimeoutOption,
    PageloadTimeoutOption,
)
from .services import WhatsappSender

app = typer.Typer()


@app.callback()
def main():
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages(
    filepath: FilepathArgument,
    messages_timeout: MessagesTimeoutOption,
    pageload_timeout: PageloadTimeoutOption,
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    with WhatsappSender(messages_timeout, pageload_timeout) as sender:
        sender.send(messages=get_messages_from_xlsx(filepath))
