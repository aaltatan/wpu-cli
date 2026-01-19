from enum import StrEnum

from .schemas import RGB, Position


class RGBName(StrEnum):
    UNKNOWN = "unknown"
    AVAILABLE_GREEN_BUTTON = "available_green_button"


COLORS: dict[RGB, RGBName] = {
    (37, 191, 102): RGBName.AVAILABLE_GREEN_BUTTON,
}

DEVICES: dict[Position, dict[str, Position]] = {
    (1920, 1200): {
        "error_ok": (700, 400),
        "send_btn": (934, 710),
    },
}
