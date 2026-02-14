# ruff: noqa: B008, PLR0913

from typer_di import Depends, TyperDI

from cli.clipboard import get_clipboard

from .dependencies import (
    Config,
    WriteOptions,
    get_choices,
    get_processor_fn,
    get_reader_data,
    get_scorer_fn,
)
from .processors import ProcessorFn
from .scorers import ScorerFn
from .services import match_list
from .writers import writers

app = TyperDI()


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("list")
def match_list_cmd(
    queries: list[str] = Depends(get_reader_data),
    choices: list[str] = Depends(get_choices),
    processor_fn: ProcessorFn = Depends(get_processor_fn),
    scorer_fn: ScorerFn = Depends(get_scorer_fn),
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

    write_fn = writers[write_options.writer]
    write_fn(config.limit, write_options.export_path, matches)


@app.command("clip")
def match_clip_cmd(
    choices: list[str] = Depends(get_choices),
    processor_fn: ProcessorFn = Depends(get_processor_fn),
    scorer_fn: ScorerFn = Depends(get_scorer_fn),
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

    write_fn = writers[write_options.writer]
    write_fn(config.limit, write_options.export_path, matches)
