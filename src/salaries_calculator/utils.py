from pathlib import Path

import openpyxl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from .controllers import Salary


class Wb:
    def __init__(self) -> None:
        self.wb: Workbook = openpyxl.Workbook()

    def _filename(self, filename: str) -> Path:
        return Path(__file__).home() / "Desktop" / filename

    def save_table(
        self,
        data: list[Salary],
        filename: str = "workbook.xlsx",
    ) -> None:
        ws: Worksheet = self.wb.active
        if ws.max_row == 1:
            headers: tuple[str] = (
                "gross_salary",
                "compensations",
                "total_salary",
                "layers_tax",
                "fixed_tax",
                "total_deductions",
                "net_salary",
                "compensations_to_total",
            )
            ws.append(headers)
        for salary in data:
            ws.append(
                [
                    salary.gross_salary,
                    salary.compensations,
                    salary.total_salary,
                    salary.tax,
                    salary.fixed_tax,
                    salary.total_deductions,
                    salary.net_salary,
                    salary.compensations_to_total,
                ]
            )
        self.wb.save(self._filename(filename))
