from dataclasses import dataclass

from cli.fuzz.processors import ProcessorFn, get_processor_fn
from cli.fuzz.readers import get_reader_data
from cli.fuzz.scorers import ScorerFn, get_scorer_fn

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


def get_reader_data_wrapper(queries_path: QueriesPathOpt) -> list[str]:
    return get_reader_data(queries_path)


@dataclass
class WriteOptions:
    export_path: ExportPathOpt
    writer: WriterOpt
