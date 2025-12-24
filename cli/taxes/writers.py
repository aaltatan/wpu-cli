# ruff: noqa: PTH123

import json
from collections.abc import Callable
from functools import wraps
from pathlib import Path

import xlwings as xw

from .constants import HEADERS
from .schemas import Salary

type WriteFn = Callable[[list[Salary], Path], None]

_write_functions: dict[str, WriteFn] = {}


def get_write_functions() -> dict[str, WriteFn]:
    return _write_functions.copy()


def get_write_fn(extension: str) -> WriteFn:
    return _write_functions[extension]


def register_extension(extension: str) -> Callable[[WriteFn], WriteFn]:
    def decorator(write_fn: WriteFn) -> WriteFn:
        @wraps(write_fn)
        def wrapper(salaries: list[Salary], path: Path) -> None:
            write_fn(salaries, path)

        _write_functions[extension] = wrapper
        return wrapper

    return decorator


def _format_as_currency(rg: xw.Range) -> None:
    rg.number_format = "###,###,###"


def _format_as_percentage(rg: xw.Range) -> None:
    rg.number_format = "0.00%"


def _format_bold(rg: xw.Range) -> None:
    rg.font.bold = True


@register_extension("xlsx")
def write_to_excel(salaries: list[Salary], path: Path) -> None:
    wb = xw.Book()
    ws = wb.sheets.active

    headers_row = [header for header, _ in HEADERS.items()]

    ws.range("A1").options(index=False).value = headers_row

    rows = [
        [
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
        for idx, salary in enumerate(salaries, start=1)
    ]

    ws.range(f"A2:A{len(rows) + 1}").options(index=False).value = rows

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
def write_to_json(salaries: list[Salary], path: Path) -> None:
    data = [json.loads(salary.model_dump_json()) for salary in salaries]

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


@register_extension("jsonl")
def write_to_jsonl(salaries: list[Salary], path: Path) -> None:
    with open(path, "w") as f:
        f.writelines(salary.model_dump_json(indent=4) + "\n" for salary in salaries)
