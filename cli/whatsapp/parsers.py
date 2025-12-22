from pathlib import Path

import pandas as pd
import typer

from cli.utils import extract_extension

from .schemas import Message


def _get_messages_from_xlsx(filepath: Path) -> list[Message]:
    messages_dict: dict[str, list[str]] = {}
    data = pd.read_excel(filepath).to_dict(orient="records")

    for row in data:
        phone, text = row.values()

        phone = str(phone)
        text = str(text).replace("_x000D_", "")

        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    return [Message(phone, texts) for phone, texts in messages_dict.items()]


def parse_messages(value: str) -> list[Message]:
    try:
        path = Path(value).resolve()
    except typer.BadParameter:
        message = "Invalid path to xlsx file"
        raise typer.BadParameter(message) from None

    if not path.exists():
        message = f"Path {path} does not exist"
        raise typer.BadParameter(message) from None

    if not path.is_file():
        message = f"Path {path} is not a file"
        raise typer.BadParameter(message) from None

    if extract_extension(path) != "xlsx":
        message = f"Path {path} is not an xlsx file"

    return _get_messages_from_xlsx(path)
