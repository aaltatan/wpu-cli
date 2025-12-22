from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from typer_di import Depends

from cli.fuzz.loaders import get_loader_data

from ._callbacks import loader_path_callback

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
        callback=loader_path_callback,
    ),
]


def _get_loader_data(queries_path: QueriesPathOpt) -> list[str]:
    return get_loader_data(queries_path)


@dataclass
class QueryOptions:
    queries: list[str] = Depends(_get_loader_data)  # noqa: RUF009
