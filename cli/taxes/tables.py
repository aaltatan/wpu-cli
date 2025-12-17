from rich.table import Table

from .constants import HEADERS
from .schemas import Salary


def get_salary_table(*salaries: Salary, title: str = "Results") -> Table:
    table = Table(title=title)

    for header, options in HEADERS.items():
        table.add_column(header, **options)  # type: ignore  # noqa: PGH003

    for idx, salary in enumerate(salaries, start=1):
        table.add_row(
            str(idx),
            f"{salary.gross:,.2f}",
            f"{salary.compensations:,.2f}",
            f"{salary.total:,.2f}",
            f"{salary.ss_deduction:,.2f}",
            f"{salary.brackets_tax:,.2f}",
            f"{salary.fixed_tax:,.2f}",
            f"{salary.taxes:,.2f}",
            f"{salary.deductions:,.2f}",
            f"{salary.net:,.2f}",
            f"{salary.compensations_to_total_ratio:.2%}",
        )

    return table
