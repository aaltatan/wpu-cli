# ruff: noqa: B008

from typer_di import Depends, TyperDI

from .dependencies import (
    Config,
    get_choices,
    get_clipboard_queries,
    get_processor_fn,
    get_queries,
    get_scorer_fn,
)
from .processors import ProcessorFn
from .scorers import ScorerFn
from .services import match_list
from .writers import writers

app = TyperDI(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Fuzz search in a given choices file."""


@app.command("list", no_args_is_help=True)
def match_list_cmd(
    queries: list[str] = Depends(get_queries),
    choices: list[str] = Depends(get_choices),
    processor_fn: ProcessorFn = Depends(get_processor_fn),
    scorer_fn: ScorerFn = Depends(get_scorer_fn),
    config: Config = Depends(Config),
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

    write_fn = writers[config.writer]
    write_fn(config.limit, config.export_path, matches)


@app.command("clip", no_args_is_help=True)
def match_clip_cmd(
    queries: list[str] = Depends(get_clipboard_queries),
    choices: list[str] = Depends(get_choices),
    processor_fn: ProcessorFn = Depends(get_processor_fn),
    scorer_fn: ScorerFn = Depends(get_scorer_fn),
    config: Config = Depends(Config),
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

    write_fn = writers[config.writer]
    write_fn(config.limit, config.export_path, matches)
