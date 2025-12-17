from pathlib import Path

import pandas as pd

from .schemas import Message


def get_messages_from_xlsx(filepath: Path) -> list[Message]:
    messages_dict: dict[str, list[str]] = {}
    data = pd.read_excel(filepath).to_dict(orient="records")

    for row in data:
        phone, text = row.values()
        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    return [Message(phone, texts) for phone, texts in messages_dict.items()]
