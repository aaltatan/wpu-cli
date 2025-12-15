from syriantaxes import Bracket


def get_brackets(
    mins: list[float], maxes: list[float], rates: list[float]
) -> list[Bracket]:
    return [
        Bracket(_min, _max, rate)
        for _min, _max, rate in zip(mins, maxes, rates, strict=True)
    ]
