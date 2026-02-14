from enum import StrEnum

type RGB = tuple[int, int, int]
type Position = tuple[int, int]


class RGBName(StrEnum):
    UNKNOWN = "unknown"
    AVAILABLE_GREEN_BUTTON = "available_green_button"


class Button(StrEnum):
    ERROR_OK = "error_ok"
    SEND = "send"


COLORS: dict[RGB, RGBName] = {
    (58, 197, 118): RGBName.AVAILABLE_GREEN_BUTTON,
}


DEVICES: dict[Position, dict[Button, Position]] = {
    (1920, 1200): {
        Button.ERROR_OK: (700, 400),
        Button.SEND: (934, 710),
    },
}
