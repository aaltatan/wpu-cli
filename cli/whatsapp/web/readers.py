from typing import Any

from .schemas import Message


def get_messages(messages: list[dict[Any, Any]]) -> list[Message]:
    messages_dict: dict[str, list[str]] = {}

    for row in messages:
        phone, text = row.values()
        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    return [Message(phone, texts) for phone, texts in messages_dict.items()]
