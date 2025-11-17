import json
from collections.abc import Callable
from enum import StrEnum
from functools import wraps
from pathlib import Path
from typing import Any

import openpyxl

from .constants import TABLE_HEADERS
from .services import Salary

type ExporterFn = Callable[[str, list[Salary], Path], Path]


class ExportType(StrEnum):
    XLSX = "xlsx"
    JSON = "json"
    JSONL = "jsonl"


_exporters: dict[ExportType, ExporterFn] = {}


def register_exporter(fmt: ExportType) -> Callable[[ExporterFn], ExporterFn]:
    def decorator(exporter_fn: ExporterFn) -> ExporterFn:
        @wraps(exporter_fn)
        def wrapper(filename: str, salaries: list[Salary], path: Path) -> Path:
            absolute_path = path / f"{filename}.{fmt.value}"
            return exporter_fn(filename, salaries, absolute_path)

        _exporters[fmt] = wrapper

        return wrapper

    return decorator


def get_exporters() -> dict[ExportType, ExporterFn]:
    return _exporters.copy()


@register_exporter(ExportType.JSON)
def export_to_json(_: str, salaries: list[Salary], path: Path) -> Path:
    data: list[dict[str, Any]] = [salary.model_dump() for salary in salaries]

    with Path.open(path, "w") as f:
        f.write(json.dumps(data, indent=4))

    return path


@register_exporter(ExportType.JSONL)
def export_to_jsonl(_: str, salaries: list[Salary], path: Path) -> Path:
    for salary in salaries:
        data = salary.model_dump()
        with Path.open(path, "a") as f:
            f.write(json.dumps(data) + "\n")

    return path


@register_exporter(ExportType.XLSX)
def export_to_excel(_: str, salaries: list[Salary], path: Path) -> Path:
    wb = openpyxl.Workbook()
    ws = wb.active

    if ws is None:
        message = "❌ Workbook is empty"
        raise ValueError(message)

    ws.append(TABLE_HEADERS)
    for idx, salary in enumerate(salaries):
        ws.append(salary.to_list(idx + 1))

    wb.save(path)

    return path
