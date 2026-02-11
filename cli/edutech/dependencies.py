from dataclasses import dataclass

from .options import EdutechPasswordOpt, EdutechUsernameOpt, FinancialYearOpt


@dataclass
class Edutech:
    username: EdutechUsernameOpt
    password: EdutechPasswordOpt
    financial_year: FinancialYearOpt
