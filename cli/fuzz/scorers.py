from collections.abc import Callable

from thefuzz.fuzz import QRatio, UQRatio, UWRatio, WRatio

from .enums import Scorer

type AsciiScorerFn = Callable[[str, str, bool, bool], int]
type UnicodeScorerFn = Callable[[str, str, bool], int]
type ScorerFn = AsciiScorerFn | UnicodeScorerFn


_scorers: dict[Scorer, ScorerFn] = {
    Scorer.QUICK_RATIO: QRatio,
    Scorer.WEIGHTED_RATIO: WRatio,
    Scorer.UNICODE_QUICK_RATIO: UQRatio,
    Scorer.UNICODE_WEIGHTED_RATIO: UWRatio,
}


def get_scorer_fn(scorer: Scorer) -> ScorerFn:
    return _scorers.get(scorer, _scorers[Scorer.WEIGHTED_RATIO])
