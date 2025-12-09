import win32clipboard as clipboard


def get_clipboard() -> str:
    clipboard.OpenClipboard()
    text = clipboard.GetClipboardData(clipboard.CF_UNICODETEXT)
    clipboard.CloseClipboard()

    if not isinstance(text, str):
        message = f"Clipboard data is not str. Got {type(text)}"
        raise TypeError(message)

    return text


def set_clipboard(text: str):
    clipboard.OpenClipboard()
    clipboard.SetClipboardText(text, clipboard.CF_UNICODETEXT)
    clipboard.CloseClipboard()
