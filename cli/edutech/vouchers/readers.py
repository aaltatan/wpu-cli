from pathlib import Path

import pandas as pd

from .options import Chapter
from .schemas import Row


def read_voucher_from_xlsx(filepath: Path, chapter: Chapter) -> list[Row]:
    data = pd.read_excel(filepath).fillna("").to_dict(orient="records")

    return [
        Row.from_kwargs(
            faculty=row["Building"],
            chapter=chapter,
            debit=row["Debit By Net"],
            credit=row["Credit By Net"],
            account_id=row["EDU@tech Account Number"],
            notes=row["Notes"],
            string_account=row["Explanation"],
            faculty_string=row["Building"],
        )
        for row in data
    ]
