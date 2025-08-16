from dataclasses import dataclass, field

import arabic_reshaper
from bidi.algorithm import get_display
from num2words import num2words


@dataclass
class PaymentOrder:
    serial: str
    name: str
    gender: str
    amount: int
    national_id: str | None = None
    amount_in_words: str = field(init=False)

    def __post_init__(self) -> None:
        self.serial = str(int(self.serial))

        amount_in_words = num2words(self.amount, lang="ar")
        reshaped_text = arabic_reshaper.reshape(amount_in_words)
        self.amount_in_words = get_display(reshaped_text)

        self.amount = f"{int(self.amount):,}"
