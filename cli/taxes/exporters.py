# ruff: noqa: PTH123

import json
from collections.abc import Callable
from functools import wraps
from pathlib import Path

import xlwings as xw

from .constants import HEADERS
from .schemas import Salary

type ExportFunc = Callable[[list[Salary], Path], None]

_export_functions: dict[str, ExportFunc] = {}


def get_exporter_functions() -> dict[str, ExportFunc]:
    return _export_functions.copy()


def get_extension(path: Path) -> str:
    return path.suffix.lower().replace(".", "")


def get_exporter_func(extension: str) -> ExportFunc:
    if extension not in _export_functions:
        message = f"Exporter {extension} not found."
        raise ValueError(message)

    return _export_functions[extension]


def register_extension(extension: str) -> Callable[[ExportFunc], ExportFunc]:
    def decorator(func: ExportFunc) -> ExportFunc:
        @wraps(func)
        def wrapper(salaries: list[Salary], path: Path) -> None:
            func(salaries, path)

        _export_functions[extension] = wrapper
        return wrapper

    return decorator


def _format_as_currency(rg: xw.Range) -> None:
    rg.number_format = "###,###,###"


def _format_as_percentage(rg: xw.Range) -> None:
    rg.number_format = "0.00%"


def _format_bold(rg: xw.Range) -> None:
    rg.font.bold = True


@register_extension("xlsx")
def export_to_excel(salaries: list[Salary], path: Path) -> None:
    wb = xw.Book()
    ws = wb.sheets.active

    headers_row = [header for header, _ in HEADERS.items()]

    ws.range("A1").options(index=False).value = headers_row

    for idx, salary in enumerate(salaries, start=1):
        ws.range(f"A{idx + 1}").options(index=False).value = [
            idx,
            float(salary.gross),
            float(salary.compensations),
            float(salary.total),
            float(salary.ss_deduction),
            float(salary.brackets_tax),
            float(salary.fixed_tax),
            float(salary.taxes),
            float(salary.deductions),
            float(salary.net),
            float(salary.compensations_to_total_ratio),
        ]

    lr = ws.range("A1").end("down").row
    lc = ws.range("A1").end("right").column

    _format_as_currency(ws.range(f"B2:J{lr}"))
    _format_as_percentage(ws.range(f"K2:K{lr}"))
    _format_bold(ws.range(f"D2:D{lr}"))
    _format_bold(ws.range(f"J2:J{lr}"))
    _format_bold(ws.range("A1", (1, lc)))
    ws.autofit()

    wb.save(path)


@register_extension("json")
def export_to_json(salaries: list[Salary], path: Path) -> None:
    data = [json.loads(salary.model_dump_json()) for salary in salaries]

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


@register_extension("jsonl")
def export_to_jsonl(salaries: list[Salary], path: Path) -> None:
    with open(path, "w") as f:
        f.writelines(
            salary.model_dump_json(indent=4) + "\n" for salary in salaries
        )
