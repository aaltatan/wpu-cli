# ruff: noqa: PTH123

import json
from collections.abc import Callable
from functools import wraps
from pathlib import Path

import xlwings as xw

from .constants import HEADERS
from .schemas import Salary

type WriteFn = Callable[[list[Salary], Path], None]


class WriteFnNotFoundError(Exception):
    def __init__(self, extension: str) -> None:
        super().__init__(f"extension of type (.{extension}) not supported.")


class WriterRegistry:
    def __init__(self) -> None:
        self._write_functions: dict[str, WriteFn] = {}

    def __contains__(self, extension: str) -> bool:
        return extension in self._write_functions

    def __getitem__(self, extension: str) -> WriteFn:
        if extension not in self._write_functions:
            raise WriteFnNotFoundError(extension)

        return self._write_functions[extension]

    def register(self, extension: str) -> Callable[[WriteFn], WriteFn]:
        def decorator(write_fn: WriteFn) -> WriteFn:
            @wraps(write_fn)
            def wrapper(salaries: list[Salary], path: Path) -> None:
                write_fn(salaries, path)

            self._write_functions[extension] = wrapper
            return wrapper

        return decorator


writer = WriterRegistry()


@writer.register("xlsx")
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

    ws.range(f"B2:J{lr}").number_format = "0.00"

    ws.range(f"K2:K{lr}").number_format = "0.00%"

    ws.range(f"D2:D{lr}").font.bold = True
    ws.range(f"J2:J{lr}").font.bold = True
    ws.range("A1", (1, lc)).font.bold = True

    ws.autofit()

    wb.save(path)


@writer.register("json")
def write_to_json(salaries: list[Salary], path: Path) -> None:
    data = [json.loads(salary.model_dump_json()) for salary in salaries]

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


@writer.register("jsonl")
def write_to_jsonl(salaries: list[Salary], path: Path) -> None:
    with open(path, "w") as f:
        f.writelines(salary.model_dump_json(indent=4) + "\n" for salary in salaries)
