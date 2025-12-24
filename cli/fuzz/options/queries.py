from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from typer_di import Depends

from cli.fuzz.readers import get_reader_data

from ._callbacks import reader_path_callback

QueriesPathOpt = Annotated[
    Path,
    typer.Option(
        "-q",
        "--queries-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the queries",
        callback=reader_path_callback,
    ),
]


def _get_reader_data_wrapper(queries_path: QueriesPathOpt) -> list[str]:
    return get_reader_data(queries_path)


@dataclass
class QueryOptions:
    queries: list[str] = Depends(_get_reader_data_wrapper)  # noqa: RUF009
