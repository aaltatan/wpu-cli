from typing import Annotated

import typer

from .callback import app_callback
from .loaders import get_clipboard_data, get_loader_data
from .options import ExportPathOption, QueriesPathOption, WriterOption
from .processors import get_processor_fn
from .scorers import get_scorer_fn
from .services import match_list, match_one
from .writers import SingleQueryTerminalWriter, get_writer_fn

app = typer.Typer(callback=app_callback)


@app.command("one")
def match_one_command(ctx: typer.Context, query: Annotated[str, typer.Argument()]):
    matches = match_one(
        query=query,
        choices=get_loader_data(ctx.obj["choices_path"]),
        processor_fn=get_processor_fn(ctx.obj["processors"] + ctx.obj["default_processors"]),
        scorer_fn=get_scorer_fn(ctx.obj["scorer"]),
        accuracy=ctx.obj["accuracy"],
        limit=ctx.obj["limit"],
        remove_duplicated=ctx.obj["remove_duplicated"],
    )

    writer = SingleQueryTerminalWriter("results", ["Score", "Match"])
    writer.write(matches)


@app.command("list")
def match_list_command(
    ctx: typer.Context,
    queries_path: QueriesPathOption,
    export_path: ExportPathOption,
    writer: WriterOption,
):
    matches = match_list(
        queries=get_loader_data(queries_path),
        choices=get_loader_data(ctx.obj["choices_path"]),
        processor_fn=get_processor_fn(ctx.obj["processors"] + ctx.obj["default_processors"]),
        scorer_fn=get_scorer_fn(ctx.obj["scorer"]),
        accuracy=ctx.obj["accuracy"],
        limit=ctx.obj["limit"],
        remove_duplicated=ctx.obj["remove_duplicated"],
    )

    write_fn = get_writer_fn(writer)
    write_fn(ctx.obj["limit"], export_path, matches)


@app.command("clip")
def match_clip_command(ctx: typer.Context, export_path: ExportPathOption, writer: WriterOption):
    matches = match_list(
        queries=get_clipboard_data(),
        choices=get_loader_data(ctx.obj["choices_path"]),
        processor_fn=get_processor_fn(ctx.obj["processors"] + ctx.obj["default_processors"]),
        scorer_fn=get_scorer_fn(ctx.obj["scorer"]),
        accuracy=ctx.obj["accuracy"],
        limit=ctx.obj["limit"],
        remove_duplicated=ctx.obj["remove_duplicated"],
    )

    write_fn = get_writer_fn(writer)
    write_fn(ctx.obj["limit"], export_path, matches)
