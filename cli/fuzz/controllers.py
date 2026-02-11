# ruff: noqa: B008, PLR0913

from typer_di import Depends, TyperDI

from cli.clipboard import get_clipboard

from .dependencies import (
    Config,
    WriteOptions,
    get_choices_wrapper,
    get_processor_fn_wrapper,
    get_reader_data_wrapper,
    get_scorer_fn_wrapper,
)
from .processors import ProcessorFn
from .scorers import ScorerFn
from .services import match_list
from .writers import get_writer_fn

app = TyperDI()


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("list")
def match_list_cmd(
    queries: list[str] = Depends(get_reader_data_wrapper),
    choices: list[str] = Depends(get_choices_wrapper),
    processor_fn: ProcessorFn = Depends(get_processor_fn_wrapper),
    scorer_fn: ScorerFn = Depends(get_scorer_fn_wrapper),
    config: Config = Depends(Config),
    write_options: WriteOptions = Depends(WriteOptions),
):
    matches = match_list(
        queries=queries,
        choices=choices,
        processor_fn=processor_fn,
        scorer_fn=scorer_fn,
        accuracy=config.accuracy,
        limit=config.limit,
        remove_duplicated=config.remove_duplicated,
    )

    write_fn = get_writer_fn(write_options.writer)
    write_fn(config.limit, write_options.export_path, matches)


@app.command("clip")
def match_clip_cmd(
    choices: list[str] = Depends(get_choices_wrapper),
    processor_fn: ProcessorFn = Depends(get_processor_fn_wrapper),
    scorer_fn: ScorerFn = Depends(get_scorer_fn_wrapper),
    config: Config = Depends(Config),
    write_options: WriteOptions = Depends(WriteOptions),
):
    queries = [line for line in get_clipboard().splitlines() if line]

    matches = match_list(
        queries=queries,
        choices=choices,
        processor_fn=processor_fn,
        scorer_fn=scorer_fn,
        accuracy=config.accuracy,
        limit=config.limit,
        remove_duplicated=config.remove_duplicated,
    )

    write_fn = get_writer_fn(write_options.writer)
    write_fn(config.limit, write_options.export_path, matches)
