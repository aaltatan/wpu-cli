from typer_di import Depends, TyperDI

from .loaders import get_messages_from_xlsx
from .options import FilepathArgument, Timeout, WhatsappUrlOption, get_timeout
from .services import open_whatsapp_page, send_whatsapp_messages

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages(
    filepath: FilepathArgument,
    whatsapp_url: WhatsappUrlOption,
    timeout: Timeout = Depends(get_timeout),  # noqa: B008
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    messages = get_messages_from_xlsx(filepath)

    with open_whatsapp_page(whatsapp_url, timeout.pageload) as page:
        send_whatsapp_messages(page, messages, timeout)
