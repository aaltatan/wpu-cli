from dataclasses import dataclass
from datetime import datetime
from inspect import signature


@dataclass
class Currency:
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
        return cls(**{
            k: v for k, v in kwargs.items() if k in cls_kwargs
        })
    
    @property
    def change(self):
        return "✅" if self.buy < self.preBuy else "❌"
    
    def to_rich_table(self):
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
