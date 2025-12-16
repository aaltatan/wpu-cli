from rich.table import Table

from .schemas import Salary


def get_salary_table(*salaries: Salary, title: str = "Results") -> Table:
    table = Table(title=title)

    table.add_column("Gross", justify="right", style="cyan")
    table.add_column("Compensations", justify="right", style="cyan")
    table.add_column("Total", justify="right", style="green")
    table.add_column("SS Deduction", justify="right", style="cyan")
    table.add_column("Brackets Tax", justify="right", style="cyan")
    table.add_column("Fixed Tax", justify="right", style="cyan")
    table.add_column("Taxes", justify="right", style="red")
    table.add_column("Deductions", justify="right", style="red")
    table.add_column("Net", justify="right", style="green")
    table.add_column("Compensations to Total Ratio", justify="right")

    for salary in salaries:
        table.add_row(
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
