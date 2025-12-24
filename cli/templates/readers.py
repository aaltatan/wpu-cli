from pathlib import Path

import pandas as pd

from .schemas import Data


class ExcelSingleRowDataReader:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def read(self) -> Data:
        df = pd.read_excel(self.filepath)
        return df.to_dict(orient="records")


class ExcelGroupedDataReader:
    def __init__(self, filepath: Path, group_key: str, *grouped_columns: str) -> None:
        self.filepath = filepath
        self.grouped_columns = grouped_columns
        self.group_key = group_key

    def read(self) -> Data:
        df = pd.read_excel(self.filepath)

        grouped_columns = set(self.grouped_columns)
        groupby_columns_list = list(set(df.columns.to_list()) - grouped_columns)

        def _generate(group: pd.DataFrame):  # noqa: ANN202
            return group[list(self.grouped_columns)].to_dict("records")

        return (
            df.groupby(groupby_columns_list)
            .apply(_generate)
            .reset_index(name=self.group_key)
            .to_dict(orient="records")
        )
