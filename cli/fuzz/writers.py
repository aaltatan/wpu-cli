from collections.abc import Callable
from functools import wraps
from pathlib import Path

import pandas as pd
import xlwings as xw
from rich.console import Console
from rich.table import Table

from .enums import Writer

type WriteFn = Callable[[int, Path, MultipleQueriesResults], None]
type MultipleQueriesResults = list[tuple[str, Results]]
type Results = list[tuple[str, int]]


_writers: dict[Writer, WriteFn] = {}


def get_writer_fn(writer: Writer) -> WriteFn:
    return _writers[writer]


def register_writer(writer: Writer) -> Callable[[WriteFn], WriteFn]:
    def decorator(writer_fn: WriteFn) -> WriteFn:
        @wraps(writer_fn)
        def wrapper(limit: int, export_path: Path, data: MultipleQueriesResults) -> None:
            writer_fn(limit, export_path, data)

        _writers[writer] = wrapper
        return wrapper

    return decorator


@register_writer(Writer.TERMINAL)
def write_terminal(columns_count: int, _: Path, results: MultipleQueriesResults) -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta", title="results")

    table.add_column("Query", justify="right")

    for idx in range(columns_count):
        table.add_column(f"Match {idx + 1}", justify="right")

    for query, r in results:
        columns = [match for match, _ in r]
        table.add_row(query, *columns)

    console.print(table)


@register_writer(Writer.FLAT_XLSX)
def write_flat_excel(
    columns_count: int, export_path: Path, results: MultipleQueriesResults
) -> None:
    data = [[query, *[match for match, _ in r]] for query, r in results]

    df = pd.DataFrame(
        data, columns=["Query"] + [f"Match {idx + 1}" for idx in range(columns_count)]
    )

    df.to_excel(export_path, index=False)


@register_writer(Writer.CHOICES_XLSX)
def write_choices_excel(_: int, export_path: Path, results: MultipleQueriesResults) -> None:
    headers = ["Query", "Matches"]
    data = [(query, [match for match, _ in r]) for query, r in results]

    wb = xw.Book()
    ws = wb.sheets.active

    ws.range("A1").options(index=False).value = headers

    for idx, (query, matches) in enumerate(data, start=2):
        formula = ",".join(matches) if matches else "#N/A"
        ws.range(f"A{idx}").options(index=False).value = query
        ws.range(f"B{idx}").api.Validation.Add(Type=3, Formula1=formula)
        ws.range(f"B{idx}").options(index=False).value = matches[0] if matches else "#N/A"

    wb.save(export_path)
