from datetime import datetime
from pathlib import Path

import xlwings as xw
from docxtpl import DocxTemplate

from .constants import MONTHS
from .schemas import PaymentOrder


def get_orders_from_excel(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int] = (2, 1),
    last_column: int = 5,
    sheet_name: str = "orders",
) -> list[list[str]]:
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

    return rg


def _generate_order_template(
    order: PaymentOrder,
    month: int,
    year: int,
    *,
    template_name: str = "order",
    foldername: str = "orders",
) -> None:
    if month not in MONTHS:
        raise ValueError(f"Invalid month: {month}")

    if year not in range(1900, 2100):
        raise ValueError(f"Invalid year: {year}")

    template = DocxTemplate(f"templates/{template_name}.docx")
    context = {
        "order": order,
        "month": MONTHS[month],
        "year": str(year),
        "today": datetime.now().strftime("%d/%m/%Y"),
    }
    template.render(context)

    home_path = Path.home().resolve()

    output_path = home_path / "Desktop" / foldername

    if not output_path.exists():
        output_path.mkdir(parents=True)

    filename = f"{order.serial} - {template_name} - {order.name}.docx"
    output_path = output_path / filename

    template.save(output_path)


def generate_order(order: PaymentOrder, month: int, year: int) -> None:
    """
    generate order template
    """
    _generate_order_template(
        order=order,
        month=month,
        year=year,
        template_name="order",
        foldername="orders",
    )


def generate_order_voucher(order: PaymentOrder, month: int, year: int) -> None:
    """
    generate order voucher template
    """
    _generate_order_template(
        order=order,
        month=month,
        year=year,
        template_name="order-voucher",
        foldername="orders-vouchers",
    )
