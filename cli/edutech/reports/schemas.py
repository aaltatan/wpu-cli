from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, computed_field, field_validator


class JournalRow(BaseModel):
    serial: Annotated[str, Field(alias="VOUCHER_NUMBER")]
    date: Annotated[datetime, Field(alias="VOUCHER_DATE")]
    kind: Annotated[str, Field(alias="VOUCHER_TYPE_NAME_SL")]
    debit: Annotated[Decimal, Field(alias="LOCAL_DEBIT")]
    credit: Annotated[Decimal, Field(alias="LOCAL_CREDIT")]
    account: Annotated[str, Field(alias="ACCOUNT_FULL_NAME_SL")]
    cost_center: Annotated[str | None, Field(alias="COST_CENTER_NAME_SL")] = (
        None
    )
    notes: Annotated[str | None, Field(alias="VOUCHER_DETAIL_NOTE")] = None

    @computed_field
    def account_id(self) -> str:
        return self.account.split(" - ")[-1]

    @field_validator("date", mode="before")
    @classmethod
    def parse_date_string(cls, value: str) -> datetime:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y")  # noqa: DTZ007
            except ValueError:
                message = f"Invalid date string: {value}"
                raise ValueError(message)  # noqa: B904

        return value
