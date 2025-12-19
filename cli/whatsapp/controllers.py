import typer

from .loaders import get_messages_from_xlsx
from .options import BaseUrlOption, FilepathArgument, MessagesTimeoutOption, PageloadTimeoutOption
from .services import WhatsappSender, WhatsappSession

app = typer.Typer()


@app.callback()
def main():
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages(
    filepath: FilepathArgument,
    base_url: BaseUrlOption,
    messages_timeout: MessagesTimeoutOption,
    pageload_timeout: PageloadTimeoutOption,
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    messages = get_messages_from_xlsx(filepath)

    with WhatsappSession(base_url) as session:
        sender = WhatsappSender(session, messages_timeout, pageload_timeout)
        sender.send(messages)
