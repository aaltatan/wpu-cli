import re
from dataclasses import dataclass, field


@dataclass
class Message:
    phone: str
    texts: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        full_number: re.Pattern = re.compile(r"^\+963\d{9}$")
        full_number_with_two_zeros: re.Pattern = re.compile(r"^00963\d{9}$")
        number_without_plus: re.Pattern = re.compile(r"^963\d{9}$")
        number_with_one_zero: re.Pattern = re.compile(r"^0\d{9}$")
        number_without_country_code: re.Pattern = re.compile(r"^\d{9}$")

        if full_number_with_two_zeros.match(self.phone):
            self.phone = self.phone.replace("00", "+")

        if number_without_plus.match(self.phone):
            self.phone = "+" + self.phone

        if number_with_one_zero.match(self.phone):
            self.phone = "+963" + self.phone[1:]

        if number_without_country_code.match(self.phone):
            self.phone = "+963" + self.phone

        if not full_number.match(self.phone):
            message = f"Invalid phone number: {self.phone}"
            raise ValueError(message)
