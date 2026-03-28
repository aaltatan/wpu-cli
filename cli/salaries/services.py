from syriantaxes import Rounder, SocialSecurity

from .models import SalaryInSchema, SettingsSchema


def calculate(
    rows: list[SalaryInSchema],
    settings: SettingsSchema,
    ss_obj: SocialSecurity,
    tax_rounder: Rounder,
    calculation_rounder: Rounder,
) -> None:
    pass
