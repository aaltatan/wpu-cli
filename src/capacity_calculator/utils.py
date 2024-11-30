from pathlib import Path

import openpyxl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from .controllers import Capacity


class Wb:
    def __init__(self) -> None:
        self.wb: Workbook = openpyxl.Workbook()

    def _filename(self, filename: str) -> Path:
        return Path(__file__).home() / "Desktop" / filename

    def save_table(
        self,
        data: list[Capacity],
        filename: str = "workbook.xlsx",
    ) -> None:
        ws: Worksheet = self.wb.active
        if ws.max_row == 1:
            headers: tuple[str] = (
                "name",
                "students_count",
                "teacher_to_student_ratio",
                "local_fulltime_specialist_count",
                "foreign_fulltime_specialist_count",
                "local_fulltime_supportive_count",
                "foreign_fulltime_supportive_count",
                "parttime_specialist_count",
                "parttime_supportive_count",
                "master_count",
                "capacity",
                "capacity_difference",
                "required_local_count",
                "local_count",
                "locality_difference",
            )
            ws.append(headers)
        for faculty in data:
            ws.append([
                faculty.name,
                faculty.students_count,
                faculty.teacher_to_student_ratio,
                faculty.local_fulltime_specialist_count,
                faculty.foreign_fulltime_specialist_count,
                faculty.local_fulltime_supportive_count,
                faculty.foreign_fulltime_supportive_count,
                faculty.parttime_specialist_count,
                faculty.parttime_supportive_count,
                faculty.master_count,
                faculty.capacity,
                faculty.capacity_difference,
                faculty.required_local_count,
                faculty.local_count,
                faculty.locality_difference,
            ])
        self.wb.save(self._filename(filename))
