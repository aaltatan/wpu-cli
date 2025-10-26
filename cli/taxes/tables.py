from rich.table import Table

from .constants import TABLE_HEADERS


def get_salaries_table(title: str = "results") -> Table:
    table = Table(show_header=True, header_style="bold magenta", title=title)

    for header in TABLE_HEADERS:
        style = "blue" if header in ["Total", "Net"] else "white"
        table.add_column(header, style=style, justify="right")

    return table