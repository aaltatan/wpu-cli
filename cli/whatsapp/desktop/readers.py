from typing import Any
from urllib.parse import quote


def get_desktop_whatsapp_hyperlinks(messages: list[dict[Any, Any]]) -> list[str]:
    hyperlinks: list[str] = []

    for message in messages:
        phone = message["phone"]
        text = quote(message["text"])
        hyperlinks.append(f"whatsapp://send?phone={phone}&text={text}")

    return hyperlinks
