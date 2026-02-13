from typing import Any
from urllib.parse import quote


def get_desktop_whatsapp_hyperlinks(
    messages: list[dict[Any, Any]], *, include_text: bool = True
) -> list[str]:
    hyperlinks: list[str] = []

    for message in messages:
        phone = message["phone"]
        text = quote(message["text"])

        url = f"whatsapp://send?phone={phone}"
        if include_text:
            url = f"{url}&text={text}"

        hyperlinks.append(url)

    return hyperlinks
