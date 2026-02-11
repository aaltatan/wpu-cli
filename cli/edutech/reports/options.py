from datetime import datetime, timezone
from typing import Annotated

import typer

AccountsOpt = Annotated[
    list[str],
    typer.Option(
        "--accounts",
        "-a",
        help="Accounts to filter voucher data by",
        default_factory=lambda: [
            "186208",
            "186209",
            "186210",
        ],
    ),
]

GridColumnsOpt = Annotated[
    list[str],
    typer.Option(
        "--columns",
        "-c",
        help="Grid columns to select",
        default_factory=lambda: [
            "tAccountName",
            "tAccountNameCode",
            "tVoucherType",
            "tVoucherNumber",
            "costCenterCol",
            "noteCol",
        ],
    ),
]

FromDateOpt = Annotated[
    datetime,
    typer.Option(
        "--from-date",
        help="From date in edutech general accounting",
        prompt="From date in edutech general accounting e.g. 2025-11-17",
        default_factory=lambda: datetime.now(timezone.utc),
    ),
]

ToDateOpt = Annotated[
    datetime,
    typer.Option(
        "--to-date",
        help="To date in edutech general accounting",
        prompt="To date in edutech general accounting e.g. 2025-11-17",
        default_factory=lambda: datetime.now(timezone.utc),
    ),
]
