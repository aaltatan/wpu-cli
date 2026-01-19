# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .options import Config, Timeout, get_desktop_whatsapp_hyperlinks_wrapper
from .services import WhatsappDesktopSender, check_numbers, send_numbers

app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using whatsapp Desktop application."""


@app.command("check")
def check_numbers_cmd(
    timeout: Timeout = Depends(Timeout),
    sender: WhatsappDesktopSender = Depends(WhatsappDesktopSender),
    messages: list[str] = Depends(get_desktop_whatsapp_hyperlinks_wrapper),
    config: Config = Depends(Config),
) -> None:
    """Check whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    check_numbers(sender, messages, timeout, block_after_error=config.block_after_error)


@app.command("send")
def send_numbers_cmd(
    timeout: Timeout = Depends(Timeout),
    sender: WhatsappDesktopSender = Depends(WhatsappDesktopSender),
    messages: list[str] = Depends(get_desktop_whatsapp_hyperlinks_wrapper),
    config: Config = Depends(Config),
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    send_numbers(sender, messages, timeout, block_after_error=config.block_after_error)
