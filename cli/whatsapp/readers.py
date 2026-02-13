from pathlib import Path
from typing import Any

import pandas as pd


def read_messages_from_xlsx(filepath: Path) -> list[dict[Any, Any]]:
    messages: list[dict[str, str]] = []
    _messages = pd.read_excel(filepath).to_dict(orient="records")

    for row in _messages:
        phone, text, *_ = row.values()

        phone = str(phone)
        text = str(text).replace("_x000D_", "")

        messages.append({"phone": phone, "text": text})

    return messages
