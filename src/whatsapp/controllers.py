import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from rich.progress import track
import xlwings as xw

from .schemas import Message


def get_messages_from_excel(
    fullname: Path,
    password: str,
    sheet_name: str,
    first_cell: tuple[int, int],
    last_column: int,
) -> list[Message]:
    """
    read messages data from excel file
    """
    wb: xw.Book = xw.Book(fullname, password=password)
    ws: xw.Sheet = wb.sheets(sheet_name)

    last_row: int = ws.range(first_cell).end("down").row
    first_row, first_col = first_cell
    next_row: int = first_row + 1

    rg_values = (next_row, first_col), (last_row, last_column)
    rg: list[list] = ws.range(*rg_values).value

    messages: list[Message] = [Message(phone, text) for phone, text in rg]

    return messages


def get_filepath(filename: str = "sheet1", extension: str = "xlsx") -> Path:
    """
    get filepath for excel file
    """
    filename = filename + "." + extension
    filepath = Path().resolve(__file__) / "data" / filename

    if not filepath.exists():
        raise FileNotFoundError(f"File `{filename}` not found")

    return filepath


def send_messages(messages: list[Message]) -> None:
    """
    send messages by playwright
    """
    total = len(messages)

    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50, headless=False)
        page = browser.new_page()
        page.goto("https://web.whatsapp.com", timeout=60000)

        input("After scanning QR code, Press any key to Continue ... ")

        for message in track(messages, description="📩 Sending", total=total):

            url: str = f"https://web.whatsapp.com/send?phone={message.phone}&text={message.text}"
            try:
                page.goto(url, timeout=60_000)
                btn_selector: str = 'button[aria-label="Send"] span[data-icon="send"]'
                page.is_visible(btn_selector)
                page.click(btn_selector)
                time.sleep(2)
            except:
                continue
