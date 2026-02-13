import time
import webbrowser
from typing import Protocol

import pyautogui as ui
from loguru import logger

from .constants import COLORS, DEVICES, RGBName
from .schemas import RGB, Position


class Timeout(Protocol):
    checking_loop: int
    after_opening: float
    between_messages: float


class WhatsappDesktopSender:
    def __init__(self) -> None:
        self.device_size = self.get_device_size()

    @staticmethod
    def get_device_size() -> Position:
        height, width = ui.size()
        return height, width

    @staticmethod
    def get_color(position: Position) -> RGB:
        x, y = position
        return ui.pixel(x, y)

    def get_send_btn_position(self) -> Position:
        if self.device_size not in DEVICES:
            message = f"Device size {self.device_size} not supported"
            raise ValueError(message)

        return DEVICES[self.device_size]["send_btn"]

    def _check_send_status(self) -> bool:
        if self.has_error_popup():
            return False

        x, y = self.get_send_btn_position()
        rgb = self.get_color((x, y))
        color = COLORS.get(rgb, RGBName.UNKNOWN)
        return color == RGBName.AVAILABLE_GREEN_BUTTON

    def check_send_status(self, timeout: int) -> bool:
        for _ in range(1, timeout + 1):
            if self._check_send_status():
                return True
            time.sleep(1)

        return False

    def has_error_popup(self) -> bool:
        x, y = DEVICES[self.device_size]["error_ok"]
        rgb = self.get_color((x, y))
        color = COLORS.get(rgb, RGBName.UNKNOWN)
        return color == RGBName.AVAILABLE_GREEN_BUTTON

    def click_send_btn(self) -> None:
        x, y = self.get_send_btn_position()
        ui.click(x, y)

    def click_error_ok_btn(self) -> None:
        x, y = DEVICES[self.device_size]["error_ok"]
        ui.click(x, y)


def send_messages(
    sender: WhatsappDesktopSender,
    hyperlinks: list[str],
    timeout: Timeout,
    *,
    block_after_error: bool,
) -> None:
    for link in hyperlinks:
        webbrowser.open(link)
        time.sleep(timeout.after_opening)

        send_status = sender.check_send_status(timeout.checking_loop)

        if send_status:
            sender.click_send_btn()

        if not send_status:
            logger.error(f"This number is not available: {link}")
            if block_after_error:
                input("Press any key to continue...")

        time.sleep(timeout.between_messages)


def check_numbers(
    sender: WhatsappDesktopSender,
    hyperlinks: list[str],
    timeout: Timeout,
    *,
    block_after_error: bool,
) -> None:
    for link in hyperlinks:
        webbrowser.open(link)
        time.sleep(timeout.after_opening)

        has_error = sender.has_error_popup()
        if has_error:
            logger.error(f"This number is not available: {link}")
            if block_after_error:
                input("Press any key to continue...")
                continue
