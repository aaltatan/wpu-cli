from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from cli.fuzz.enums import AdditionalProcessor, DefaultProcessor, Scorer
from cli.fuzz.processors import ProcessorFn, get_processor_fn
from cli.fuzz.readers import get_reader_data
from cli.fuzz.scorers import ScorerFn, get_scorer_fn

from ._callbacks import reader_path_callback

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
        callback=reader_path_callback,
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


def get_choices_wrapper(choices_path: ChoicesPathOpt) -> list[str]:
    return get_reader_data(choices_path)


def get_processor_fn_wrapper(
    processors: ProcessorOpt, default_processors: DefaultProcessorOpt
) -> ProcessorFn:
    return get_processor_fn(processors + default_processors)


def get_scorer_fn_wrapper(scorer: ScorerOpt) -> ScorerFn:
    return get_scorer_fn(scorer)


@dataclass
class Config:
    accuracy: AccuracyOpt
    limit: LimitOpt
    remove_duplicated: RemoveDuplicatedOpt
