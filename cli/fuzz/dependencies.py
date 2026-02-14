from dataclasses import dataclass

import typer

from cli.clipboard import get_clipboard
from cli.fuzz.processors import ProcessorFn, processors
from cli.fuzz.readers import readers
from cli.fuzz.scorers import ScorerFn
from cli.fuzz.scorers import get_scorer_fn as _get_scorer_fn

from .options import (
    AccuracyOpt,
    ChoicesPathOpt,
    DefaultProcessorOpt,
    ExportPathOpt,
    LimitOpt,
    ProcessorOpt,
    QueriesPathOpt,
    RemoveDuplicatedOpt,
    ScorerOpt,
    WriterOpt,
)


def get_choices(choices_path: ChoicesPathOpt) -> list[str]:
    return readers.get_reader_data(choices_path)


def get_processor_fn(
    processors_option: ProcessorOpt, default_processors: DefaultProcessorOpt
) -> ProcessorFn:
    return processors.get_processor_fn(processors_option + default_processors)


def get_scorer_fn(scorer: ScorerOpt) -> ScorerFn:
    return _get_scorer_fn(scorer)


@dataclass
class Config:
    accuracy: AccuracyOpt
    limit: LimitOpt
    remove_duplicated: RemoveDuplicatedOpt


def get_reader_data(queries_path: QueriesPathOpt) -> list[str]:
    return readers.get_reader_data(queries_path)


@dataclass
class WriteOptions:
    export_path: ExportPathOpt
    writer: WriterOpt


def get_clipboard_queries() -> list[str]:
    try:
        return [line for line in get_clipboard().splitlines() if line]
    except TypeError as e:
        message = "Clipboard is empty"
        raise typer.BadParameter(message) from e
