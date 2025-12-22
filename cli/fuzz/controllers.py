# ruff: noqa: B008

from typing import Annotated

import typer
from typer_di import Depends, TyperDI

from .loaders import get_clipboard_data, get_loader_data
from .options import ExportPathOption, Options, QueriesPathOption, WriterOption, get_options
from .services import match_list, match_one
from .writers import SingleQueryTerminalWriter, get_writer_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("one")
def match_one_command(
    query: Annotated[str, typer.Argument()], options: Options = Depends(get_options)
):
    matches = match_one(
        query=query,
        choices=options.choices,
        processor_fn=options.processor_fn,
        scorer_fn=options.scorer_fn,
        accuracy=options.accuracy,
        limit=options.limit,
        remove_duplicated=options.remove_duplicated,
    )

    writer = SingleQueryTerminalWriter("results", ["Score", "Match"])
    writer.write(matches)


@app.command("list")
def match_list_command(
    queries_path: QueriesPathOption,
    export_path: ExportPathOption,
    writer: WriterOption,
    options: Options = Depends(get_options),
):
    matches = match_list(
        queries=get_loader_data(queries_path),
        choices=options.choices,
        processor_fn=options.processor_fn,
        scorer_fn=options.scorer_fn,
        accuracy=options.accuracy,
        limit=options.limit,
        remove_duplicated=options.remove_duplicated,
    )

    write_fn = get_writer_fn(writer)
    write_fn(options.limit, export_path, matches)


@app.command("clip")
def match_clip_command(
    export_path: ExportPathOption, writer: WriterOption, options: Options = Depends(get_options)
):
    matches = match_list(
        queries=get_clipboard_data(),
        choices=options.choices,
        processor_fn=options.processor_fn,
        scorer_fn=options.scorer_fn,
        accuracy=options.accuracy,
        limit=options.limit,
        remove_duplicated=options.remove_duplicated,
    )

    write_fn = get_writer_fn(writer)
    write_fn(options.limit, export_path, matches)
