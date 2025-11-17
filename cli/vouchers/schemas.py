from dataclasses import InitVar, dataclass, field
from inspect import signature
from typing import Any, Literal, Self


@dataclass
class AutomataRow:
    debit: str = ""
    credit: str = ""
    account_id: str = ""
    cost_center: str = ""
    notes: str = ""


@dataclass
class Row:
    faculty: InitVar[str]
    chapter: InitVar[Literal["1", "2", "3"]]

    debit: str = "0"
    credit: str = "0"
    account_id: str = "15322"
    cost_center: str = field(init=False)
    notes: str = ""

    def __post_init__(self, faculty: str, chapter: str) -> None:
        self.debit = str(int(self.debit or 0))
        self.credit = str(int(self.credit or 0))
        self.account_id = str(int(self.account_id or 15322))

        if self.account_id.startswith("1") or self.account_id.startswith("2"):
            self.cost_center = ""
        else:
            self.cost_center = self.cost_centers.get(faculty, "11") + chapter

    @classmethod
    def from_kwargs(cls, **kwargs: dict[str, Any]) -> Self:
        params = signature(cls).parameters

        class_params = {k: v for k, v in kwargs.items() if k in params}
        meta = {k: v for k, v in kwargs.items() if k not in params}

        notes: str = class_params.get("notes") or ""

        class_params["notes"] = (
            notes + "\n" + "\n".join([v for v in meta.values() if v])
        )

        return cls(**class_params)

    @property
    def cost_centers(self) -> dict[str, str]:
        return {
            "Employee": "11",
            "Architecture": "12",
            "Management": "13",
            "Engineering": "14",
            "Dentistry": "15",
            "Dentist Clinics": "15",
            "Pharmacy": "16",
            "Civil": "17",
        }
