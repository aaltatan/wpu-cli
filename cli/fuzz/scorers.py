from collections.abc import Callable
from enum import StrEnum

from thefuzz.fuzz import QRatio, UQRatio, UWRatio, WRatio

type AsciiScorerFn = Callable[[str, str, bool, bool], int]
type UnicodeScorerFn = Callable[[str, str, bool], int]
type ScorerFn = AsciiScorerFn | UnicodeScorerFn


class Scorer(StrEnum):
    QUICK_RATIO = "q"
    UNICODE_QUICK_RATIO = "uq"
    WEIGHTED_RATIO = "w"
    UNICODE_WEIGHTED_RATIO = "uw"

    def __str__(self) -> str:
        return self.value


_scorers: dict[Scorer, ScorerFn] = {
    Scorer.QUICK_RATIO: QRatio,
    Scorer.WEIGHTED_RATIO: WRatio,
    Scorer.UNICODE_QUICK_RATIO: UQRatio,
    Scorer.UNICODE_WEIGHTED_RATIO: UWRatio,
}


def get_scorer_fn(scorer: Scorer) -> ScorerFn:
    return _scorers.get(scorer, _scorers[Scorer.WEIGHTED_RATIO])
