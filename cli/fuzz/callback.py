# ruff: noqa: PLR0913

import typer

from .options import (
    AccuracyOption,
    ChoicesPathOption,
    DefaultProcessorOption,
    LimitOption,
    ProcessorOption,
    RemoveDuplicatedOption,
    ScorerOption,
)


def app_callback(
    ctx: typer.Context,
    choices_path: ChoicesPathOption,
    processors: ProcessorOption,
    default_processors: DefaultProcessorOption,
    accuracy: AccuracyOption,
    limit: LimitOption,
    remove_duplicated: RemoveDuplicatedOption,
    scorer: ScorerOption,
):
    """Fuzz search in a given choices file."""
    ctx.obj = {
        "choices_path": choices_path,
        "processors": processors,
        "default_processors": default_processors,
        "accuracy": accuracy,
        "limit": limit,
        "remove_duplicated": remove_duplicated,
        "scorer": scorer,
    }
