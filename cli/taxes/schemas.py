from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field


class Salary(BaseModel):
    model_config = ConfigDict(
        json_encoders={Decimal: float},
    )

    gross: Decimal = Decimal(0)
    compensations: Decimal = Decimal(0)
    ss_deduction: Decimal = Decimal(0)
    brackets_tax: Decimal = Decimal(0)
    fixed_tax: Decimal = Decimal(0)

    @computed_field
    @property
    def total(self) -> Decimal:
        return self.gross + self.compensations

    @computed_field
    @property
    def taxes(self) -> Decimal:
        return self.brackets_tax + self.fixed_tax

    @computed_field
    @property
    def deductions(self) -> Decimal:
        return self.ss_deduction + self.taxes

    @computed_field
    @property
    def net(self) -> Decimal:
        return self.total - self.deductions

    @computed_field
    @property
    def compensations_to_total_ratio(self) -> Decimal:
        return self.compensations / self.total
