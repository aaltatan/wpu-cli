from dataclasses import InitVar, dataclass, field
from datetime import datetime
from inspect import signature


@dataclass
class SpTodayExchangeRate:
    currency: str
    currency_symbol: str
    purchase: int
    sale: int

    def __post_init__(self):
        self.currency = self.currency.strip()
        self.purchase = int(self.purchase)
        self.sale = int(self.sale)

    def to_rich_row(self) -> tuple[str]:
        return (
            self.currency,
            self.currency_symbol,
            f"{self.purchase:,}",
            f"{self.sale:,}",
        )


@dataclass
class CentralBankExchangeRate:
    date_str: InitVar[str] = ""
    rate_str: InitVar[str] = ""

    date: datetime = field(init=False)
    rate: int = field(init=False)

    def __post_init__(self, date_str: str, rate_str: str) -> None:
        self.date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        self.rate = int(rate_str.strip().split(".")[0])

    def to_rich_row(self) -> tuple[str]:
        return (
            self.date.strftime("%Y-%m-%d"),
            f"{self.rate:,}",
        )


@dataclass
class DollarLiraCurrency:
    title: str
    code: str
    type: str
    sell: int
    preSell: int
    buy: int
    preBuy: int
    updatedAt: str | datetime

    @classmethod
    def from_kwargs(cls, **kwargs):
        cls_kwargs = signature(cls).parameters
        return cls(**{k: v for k, v in kwargs.items() if k in cls_kwargs})

    @property
    def change(self):
        return "✅" if self.buy < self.preBuy else "❌"

    def to_rich_row(self):
        return [
            f"{self.preBuy:,}",
            f"{self.preSell:,}",
            f"{self.buy:,}",
            f"{self.sell:,}",
            self.change,
            self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
            self.title,
        ]

    def __post_init__(self):
        self.title = self.title.strip()

        self.updatedAt = datetime.strptime(
            self.updatedAt.split(".")[0], "%Y-%m-%dT%H:%M:%S"
        )
