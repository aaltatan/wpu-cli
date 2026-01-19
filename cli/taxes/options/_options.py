from typing import Annotated

import typer

CompensationsRateOpt = Annotated[
    float,
    typer.Option(
        "-r",
        "--compensations-rate",
        envvar="TAXES_DEFAULT_COMPENSATIONS_RATE",
    ),
]
