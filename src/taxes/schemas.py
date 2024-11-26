from dataclasses import dataclass, field


@dataclass
class Tax:
    name: str
    description: str
    id: int | None = None


@dataclass
class Layer:
    from_: int
    to_: int
    rate: float = 0.0
    id: int | None = None
    tax_id: int | None = None
    tax_name: str | None = None
    tax: int = field(init=False)

    def __post_init__(self):
        if self.rate < 0 or self.rate > 1:
            raise ValueError("rate must be between -1 and 1")

        if self.from_ > self.to_:
            raise ValueError("`from_` must be less than `to`")

        self.tax = (self.to_ - self.from_) * self.rate
