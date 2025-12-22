# ruff: noqa: RUF009

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from typer_di import Depends

from cli.fuzz.enums import AdditionalProcessor, DefaultProcessor, Scorer
from cli.fuzz.loaders import get_loader_data
from cli.fuzz.processors import ProcessorFn, get_processor_fn
from cli.fuzz.scorers import ScorerFn, get_scorer_fn

from ._callbacks import loader_path_callback

ChoicesPathOpt = Annotated[
    Path,
    typer.Option(
        "-c",
        "--choices-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the choices",
        callback=loader_path_callback,
    ),
]

ProcessorOpt = Annotated[
    list[AdditionalProcessor],
    typer.Option(
        "-p",
        "--processor",
        default_factory=list,
    ),
]

DefaultProcessorOpt = Annotated[
    list[DefaultProcessor],
    typer.Option(
        "--default-processor",
        default_factory=lambda: [
            DefaultProcessor["GENERAL"],
            DefaultProcessor["ARABIC"],
        ],
    ),
]

ScorerOpt = Annotated[
    Scorer,
    typer.Option(
        "-s",
        "--scorer",
        envvar="FUZZ_DEFAULT_SCORER",
        help="q for Quick Ratio, w for Weighted Ratio, u for unicode",
    ),
]

AccuracyOpt = Annotated[
    int,
    typer.Option(
        "-a",
        "--accuracy",
        envvar="FUZZ_DEFAULT_ACCURACY",
        help="Accuracy for fuzzy matching 1 to 100",
    ),
]

LimitOpt = Annotated[
    int,
    typer.Option(
        "-l",
        "--limit",
        envvar="FUZZ_DEFAULT_LIMIT",
        help="Limit for matching results",
    ),
]

RemoveDuplicatedOpt = Annotated[
    bool,
    typer.Option(
        "--remove-duplicated",
        envvar="FUZZ_DEFAULT_REMOVE_DUPLICATED",
        help="Remove duplicated results",
    ),
]


def _get_choices(choices_path: ChoicesPathOpt) -> list[str]:
    return get_loader_data(choices_path)


def _get_processor_fn(
    processors: ProcessorOpt, default_processors: DefaultProcessorOpt
) -> ProcessorFn:
    return get_processor_fn(processors + default_processors)


def _get_scorer_fn(scorer: ScorerOpt) -> ScorerFn:
    return get_scorer_fn(scorer)


@dataclass
class Options:
    accuracy: AccuracyOpt
    limit: LimitOpt
    remove_duplicated: RemoveDuplicatedOpt

    choices: list[str] = Depends(_get_choices)
    processor_fn: ProcessorFn = Depends(_get_processor_fn)
    scorer_fn: ScorerFn = Depends(_get_scorer_fn)
