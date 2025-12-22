# ruff: noqa: B008

from typing import Annotated

import typer
from typer_di import Depends, TyperDI

from .loaders import get_clipboard_data, get_loader_data
from .options import ExportPathOpt, Options, QueriesPathOpt, WriterOpt, get_options
from .services import match_list, match_one
from .writers import SingleQueryTerminalWriter, get_writer_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("one")
def match_one_cmd(query: Annotated[str, typer.Argument()], options: Options = Depends(get_options)):
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
def match_list_cmd(
    queries_path: QueriesPathOpt,
    export_path: ExportPathOpt,
    writer: WriterOpt,
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
def match_clip_cmd(
    export_path: ExportPathOpt, writer: WriterOpt, options: Options = Depends(get_options)
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
