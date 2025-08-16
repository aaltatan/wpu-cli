from datetime import datetime
from pathlib import Path

import xlwings as xw
from docxtpl import DocxTemplate

from .schemas import PaymentOrder


def get_orders_from_excel(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int] = (2, 1),
    last_column: int = 5,
    sheet_name: str = "orders",
) -> list[PaymentOrder]:
    """
    read orders data from excel file
    """
    wb = xw.Book(filepath, password=password)
    ws: xw.Sheet = wb.sheets[sheet_name]

    last_row: int = ws.range(start_cell).end("down").row

    start_row, start_col = start_cell

    rg_values: tuple[tuple[int, int], tuple[int, int]] = (
        (start_row, start_col),
        (last_row, last_column),
    )

    rg = ws.range(*rg_values).value

    orders = []

    for row in rg:
        serial, name, gender, amount, national_id = row
        order = PaymentOrder(
            serial=serial,
            name=name,
            gender=gender,
            amount=amount,
            national_id=national_id,
        )
        orders.append(order)

    return orders


def generate_order_template(order: PaymentOrder) -> None:
    """
    generate order template
    """
    template = DocxTemplate("templates/order.docx")
    context = {
        "order": order,
        "today": datetime.now().strftime("%d/%m/%Y"),
    }
    template.render(context)

    home_path = Path.home().resolve()

    output_path = home_path / "Desktop" / "orders"

    if not output_path.exists():
        output_path.mkdir(parents=True)

    output_path = output_path / f"{order.name}.docx"

    template.save(output_path)
