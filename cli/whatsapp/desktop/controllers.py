# ruff: noqa: B008
from dataclasses import dataclass

from typer_di import Depends, TyperDI

from cli.whatsapp.options import FilepathArg
from cli.whatsapp.readers import read_messages_from_xlsx

from .options import (
    AfterOpeningTimeoutOpt,
    BetweenMessagesTimeoutOpt,
    BlockAfterErrorOpt,
    CheckingLoopTimeoutOpt,
)
from .readers import get_desktop_whatsapp_hyperlinks
from .services import WhatsappDesktopSender, check_numbers, send_messages


@dataclass
class Timeout:
    checking_loop: CheckingLoopTimeoutOpt
    after_opening: AfterOpeningTimeoutOpt
    between_messages: BetweenMessagesTimeoutOpt


@dataclass
class Config:
    block_after_error: BlockAfterErrorOpt = True


def get_desktop_whatsapp_hyperlinks_check(filepath: FilepathArg) -> list[str]:
    messages = read_messages_from_xlsx(filepath)
    return get_desktop_whatsapp_hyperlinks(messages, include_text=False)


def get_desktop_whatsapp_hyperlinks_send(filepath: FilepathArg) -> list[str]:
    messages = read_messages_from_xlsx(filepath)
    return get_desktop_whatsapp_hyperlinks(messages, include_text=True)


app = TyperDI()


@app.callback()
def main() -> None:
    """Send whatsapp bulk messages using whatsapp Desktop application."""


@app.command("check")
def check_numbers_cmd(
    timeout: Timeout = Depends(Timeout),
    sender: WhatsappDesktopSender = Depends(WhatsappDesktopSender),
    messages: list[str] = Depends(get_desktop_whatsapp_hyperlinks_check),
    config: Config = Depends(Config),
) -> None:
    """Check whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    check_numbers(sender, messages, timeout, block_after_error=config.block_after_error)


@app.command("send")
def send_numbers_cmd(
    timeout: Timeout = Depends(Timeout),
    sender: WhatsappDesktopSender = Depends(WhatsappDesktopSender),
    messages: list[str] = Depends(get_desktop_whatsapp_hyperlinks_send),
    config: Config = Depends(Config),
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    send_messages(sender, messages, timeout, block_after_error=config.block_after_error)
