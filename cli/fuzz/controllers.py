# ruff: noqa: PLR0913

from typing import Annotated

import typer

from .loaders import get_clipboard_data, get_loader_data
from .options import (
    AccuracyOption,
    ChoicesPathOption,
    DefaultProcessorOption,
    ExportPathOption,
    LimitOption,
    ProcessorOption,
    QueriesPathOption,
    RemoveDuplicatedOption,
    ScorerOption,
    WriterOption,
)
from .processors import get_processor_func
from .scorers import get_scorer_func
from .services import match_list, match_one
from .writers import SingleQueryTerminalWriter, get_writer_func

app = typer.Typer()


@app.command("one")
def match_one_command(
    query: Annotated[str, typer.Argument()],
    choices_path: ChoicesPathOption,
    processors: ProcessorOption,
    default_processors: DefaultProcessorOption,
    accuracy: AccuracyOption,
    limit: LimitOption,
    remove_duplicated: RemoveDuplicatedOption,
    scorer: ScorerOption,
):
    matches = match_one(
        query=query,
        choices=get_loader_data(choices_path),
        processor_fn=get_processor_func(processors + default_processors),
        scorer_fn=get_scorer_func(scorer),
        accuracy=accuracy,
        limit=limit,
        remove_duplicated=remove_duplicated,
    )

    writer = SingleQueryTerminalWriter("results", ["Score", "Match"])
    writer.write(matches)


@app.command("list")
def match_list_command(
    queries_path: QueriesPathOption,
    choices_path: ChoicesPathOption,
    export_path: ExportPathOption,
    processors: ProcessorOption,
    default_processors: DefaultProcessorOption,
    scorer: ScorerOption,
    accuracy: AccuracyOption,
    limit: LimitOption,
    remove_duplicated: RemoveDuplicatedOption,
    writer: WriterOption,
):
    matches = match_list(
        queries=get_loader_data(queries_path),
        choices=get_loader_data(choices_path),
        processor_fn=get_processor_func(processors + default_processors),
        scorer_fn=get_scorer_func(scorer),
        accuracy=accuracy,
        limit=limit,
        remove_duplicated=remove_duplicated,
    )

    write_fn = get_writer_func(writer)
    write_fn(limit, export_path, matches)


@app.command("clip")
def match_clip_command(
    choices_path: ChoicesPathOption,
    export_path: ExportPathOption,
    processors: ProcessorOption,
    default_processors: DefaultProcessorOption,
    scorer: ScorerOption,
    accuracy: AccuracyOption,
    limit: LimitOption,
    remove_duplicated: RemoveDuplicatedOption,
    writer: WriterOption,
):
    matches = match_list(
        queries=get_clipboard_data(),
        choices=get_loader_data(choices_path),
        processor_fn=get_processor_func(processors + default_processors),
        scorer_fn=get_scorer_func(scorer),
        accuracy=accuracy,
        limit=limit,
        remove_duplicated=remove_duplicated,
    )

    write_fn = get_writer_func(writer)
    write_fn(limit, export_path, matches)
