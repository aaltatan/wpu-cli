import re


def validate_financial_year(year: str) -> None:
    pattern = re.compile(r"^20\d{2}/20\d{2}$")

    if not pattern.match(year):
        message = (
            f"Invalid financial year: {year} you should use format 2025/2026"
        )
        raise ValueError(message)

    last_year, current_year = year.split("/")

    if int(last_year) >= int(current_year):
        message = f"Invalid financial year: {year}"
        raise ValueError(message)
