from collections.abc import Callable, Collection
from enum import StrEnum
from functools import wraps
from pathlib import Path

import pandas as pd
import xlwings as xw
from rich.console import Console
from rich.table import Table

type WriteFunc = Callable[[int, Path, MultipleQueriesResults], None]
type MultipleQueriesResults = list[tuple[str, Results]]
type Results = list[tuple[str, int]]


class Writer(StrEnum):
    TERMINAL = "terminal"
    FLAT_XLSX = "flat-xlsx"
    CHOICES_XLSX = "choices-xlsx"

    def __str__(self) -> str:
        return self.value


_writers: dict[Writer, WriteFunc] = {}


def get_writer_func(writer: Writer) -> WriteFunc:
    return _writers[writer]


def register_writer(writer: Writer) -> Callable[[WriteFunc], WriteFunc]:
    def decorator(writer_func: WriteFunc) -> WriteFunc:
        @wraps(writer_func)
        def wrapper(
            limit: int, export_path: Path, data: MultipleQueriesResults
        ) -> None:
            writer_func(limit, export_path, data)

        _writers[writer] = wrapper
        return wrapper

    return decorator


@register_writer(Writer.TERMINAL)
def write_terminal(
    columns_count: int, _: Path, results: MultipleQueriesResults
) -> None:
    console = Console()
    table = Table(
        show_header=True, header_style="bold magenta", title="results"
    )

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
        data,
        columns=["Query"]
        + [f"Match {idx + 1}" for idx in range(columns_count)],
    )

    df.to_excel(export_path, index=False)


@register_writer(Writer.CHOICES_XLSX)
def write_choices_excel(
    _: int, export_path: Path, results: MultipleQueriesResults
) -> None:
    headers = ["Query", "Matches"]
    data = [(query, [match for match, _ in r]) for query, r in results]

    wb = xw.Book()
    ws = wb.sheets.active

    ws.range("A1").options(index=False).value = headers

    for idx, (query, matches) in enumerate(data, start=2):
        formula = ",".join(matches)
        ws.range(f"A{idx}").options(index=False).value = query
        ws.range(f"B{idx}").api.Validation.Add(Type=3, Formula1=formula)
        ws.range(f"B{idx}").options(index=False).value = matches[0]

    wb.save(export_path)


class SingleQueryTerminalWriter:
    def __init__(self, title: str, headers: Collection[str]) -> None:
        self.title = title
        self.headers = headers

    def get_table(self) -> Table:
        table = Table(
            show_header=True, header_style="bold magenta", title=self.title
        )

        for header in self.headers:
            table.add_column(header, justify="right")

        return table

    def write(self, results: Results) -> None:
        console = Console()
        table = self.get_table()

        for match, score in results:
            table.add_row(str(score), match)

        console.print(table)
