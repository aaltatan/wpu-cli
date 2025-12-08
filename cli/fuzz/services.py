# ruff: noqa: PLR0913

from collections.abc import Callable, Collection

from thefuzz.process import extract

type Results = list[tuple[str, int]]


def _remove_duplicated_results(results: Results) -> Results:
    non_duplicated_results: Results = []

    for match, score in results:
        if (match, score) not in non_duplicated_results:
            non_duplicated_results.append((match, score))

    return non_duplicated_results


def _filter_by_accuracy(results: Results, accuracy: int) -> Results:
    return [(match, score) for match, score in results if score >= accuracy]


def match_one(
    query: str,
    choices: Collection[str],
    processor_fn: Callable,
    scorer_fn: Callable,
    *,
    remove_duplicated: bool,
    accuracy: int | None = None,
    limit: int | None = None,
) -> Results:
    if limit is None:
        limit = len(choices)

    results = extract(query, choices, processor_fn, scorer_fn, limit)

    if not isinstance(results, list):
        message = f"Unexpected results type: {type(results)}"
        raise TypeError(message)

    if remove_duplicated:
        results = _remove_duplicated_results(results)

    if accuracy is not None:
        results = _filter_by_accuracy(results, accuracy)

    return results


def match_all(
    queries: Collection[str],
    choices: Collection[str],
    processor_fn: Callable,
    scorer_fn: Callable,
    *,
    remove_duplicated: bool,
    accuracy: int | None = None,
    limit: int | None = None,
) -> list[tuple[str, Results]]:
    return [
        (
            query,
            match_one(
                query,
                choices,
                processor_fn,
                scorer_fn,
                remove_duplicated=remove_duplicated,
                accuracy=accuracy,
                limit=limit,
            ),
        )
        for query in queries
    ]
