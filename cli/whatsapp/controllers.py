import typer

from .loaders import get_messages_from_xlsx
from .options import (
    FilepathArgument,
    MessagesTimeoutOption,
    PageloadTimeoutOption,
    WhatsappUrlOption,
)
from .services import open_whatsapp_page, send_whatsapp_messages

app = typer.Typer()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages(
    filepath: FilepathArgument,
    whatsapp_url: WhatsappUrlOption,
    messages_timeout: MessagesTimeoutOption,
    pageload_timeout: PageloadTimeoutOption,
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    messages = get_messages_from_xlsx(filepath)

    with open_whatsapp_page(whatsapp_url) as page:
        send_whatsapp_messages(page, messages, messages_timeout, pageload_timeout)
