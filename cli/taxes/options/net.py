from dataclasses import dataclass
from typing import Annotated

import typer

from ._options import CompensationsRateOpt

TargetSalaryArg = Annotated[float, typer.Argument()]


@dataclass
class NetOptions:
    target_salary: TargetSalaryArg
    compensations_rate: CompensationsRateOpt
