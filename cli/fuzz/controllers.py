# ruff: noqa: B008

from typer_di import Depends, TyperDI

from cli.clipboard import get_clipboard

from .options import Options, QueryOptions, WriteOptions
from .services import match_list
from .writers import get_writer_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("list")
def match_list_cmd(
    options: Options = Depends(Options),
    query_options: QueryOptions = Depends(QueryOptions),
    write_options: WriteOptions = Depends(WriteOptions),
):
    matches = match_list(
        queries=query_options.queries,
        choices=options.choices,
        processor_fn=options.processor_fn,
        scorer_fn=options.scorer_fn,
        accuracy=options.accuracy,
        limit=options.limit,
        remove_duplicated=options.remove_duplicated,
    )

    write_fn = get_writer_fn(write_options.writer)
    write_fn(options.limit, write_options.export_path, matches)


@app.command("clip")
def match_clip_cmd(
    options: Options = Depends(Options),
    write_options: WriteOptions = Depends(WriteOptions),
):
    queries = [line for line in get_clipboard().splitlines() if line]

    matches = match_list(
        queries=queries,
        choices=options.choices,
        processor_fn=options.processor_fn,
        scorer_fn=options.scorer_fn,
        accuracy=options.accuracy,
        limit=options.limit,
        remove_duplicated=options.remove_duplicated,
    )

    write_fn = get_writer_fn(write_options.writer)
    write_fn(options.limit, write_options.export_path, matches)
