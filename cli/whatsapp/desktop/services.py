import time
import webbrowser
from typing import Protocol

import pyautogui as ui
from loguru import logger

from .constants import COLORS, DEVICES, RGB, Button, Position, RGBName


class DeviceNotSupportedError(Exception):
    def __init__(self, device_size: Position) -> None:
        width, height = device_size
        message = f"Device size {width}x{height} not supported"
        super().__init__(message)


class Timeout(Protocol):
    checking_loop: int
    after_opening: float
    between_messages: float


class WhatsappDesktopSender:
    def __init__(self) -> None:
        self.device_size = self._get_device_size()

    def check_send_status(self, timeout: int) -> bool:
        for _ in range(1, timeout + 1):
            if (
                not self.has_error_popup()
                and self._get_rgb(Button.SEND) == RGBName.AVAILABLE_GREEN_BUTTON
            ):
                return True
            time.sleep(1)

        return False

    def has_error_popup(self) -> bool:
        return self._get_rgb(Button.ERROR_OK) == RGBName.AVAILABLE_GREEN_BUTTON

    def click_send_btn(self) -> None:
        self._click_btn(Button.SEND)

    def _click_btn(self, button: Button) -> None:
        x, y = self._get_btn_position(button)
        ui.click(x, y)

    def _get_device_size(self) -> Position:
        height, width = ui.size()
        return height, width

    def _get_color(self, position: Position) -> RGB:
        x, y = position
        return ui.pixel(x, y)

    def _get_btn_position(self, button: Button) -> Position:
        if self.device_size not in DEVICES:
            raise DeviceNotSupportedError(self.device_size)

        return DEVICES[self.device_size][button]

    def _get_rgb(self, button: Button) -> RGBName:
        position = self._get_btn_position(button)
        color = self._get_color(position)
        return COLORS.get(color, RGBName.UNKNOWN)


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
