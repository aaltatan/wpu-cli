from dataclasses import dataclass

from rich.console import Console
from syriantaxes import Bracket, Rounder, SocialSecurity
from typer_di import Depends

from .options import (
    BracketMaxesOpt,
    BracketMinsOpt,
    BracketRatesOpt,
    CompensationsRateOpt,
    FixedTaxRateOpt,
    GrossCompensationsArg,
    GrossSalaryArg,
    MinAllowedSalaryOpt,
    MinSsAllowedSalaryOpt,
    SocialSecuritySalaryOpt,
    SsDeductionRateOpt,
    SsRoundingMethodOpt,
    SsRoundToNearestOpt,
    StartAmountRangeArg,
    StepAmountRangeArg,
    StopAmountRangeArg,
    TargetSalaryArg,
    TaxesRoundingMethodOpt,
    TaxesRoundToNearestOpt,
)


@dataclass
class Net:
    target_salary: TargetSalaryArg
    compensations_rate: CompensationsRateOpt


@dataclass
class Gross:
    salary: GrossSalaryArg
    compensations: GrossCompensationsArg = 0
    ss_salary: SocialSecuritySalaryOpt = None


@dataclass
class Config:
    min_allowed_salary: MinAllowedSalaryOpt
    fixed_tax_rate: FixedTaxRateOpt


@dataclass
class AmountRange:
    compensations_rate: CompensationsRateOpt
    start: StartAmountRangeArg
    stop: StopAmountRangeArg = None
    step: StepAmountRangeArg = None


def get_brackets(
    mins: BracketMinsOpt, maxes: BracketMaxesOpt, rates: BracketRatesOpt
) -> list[Bracket]:
    return [Bracket(mins, maxs, rate) for mins, maxs, rate in zip(mins, maxes, rates, strict=True)]


def get_taxes_rounder(
    method: TaxesRoundingMethodOpt, to_nearest: TaxesRoundToNearestOpt
) -> Rounder:
    return Rounder(method, to_nearest)


def get_ss_rounder(
    ss_rounding_method: SsRoundingMethodOpt, ss_rounding_to_nearest: SsRoundToNearestOpt
) -> Rounder:
    return Rounder(ss_rounding_method, ss_rounding_to_nearest)


def get_ss_obj(
    min_salary: MinSsAllowedSalaryOpt,
    deduction_rate: SsDeductionRateOpt,
    rounder: Rounder = Depends(get_ss_rounder),  # noqa: B008
) -> SocialSecurity:
    return SocialSecurity(min_salary, deduction_rate, rounder)


def get_console() -> Console:
    return Console()
