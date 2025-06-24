import httpx

from .schemas import Currency


def get_currencies() -> list[Currency]:
    response = httpx.get("https://dollar-lira.com/syrian-exchange/updates/updates.json")

    data: dict = response.json()

    currencies = data.get("currencies", [])
    currencies = [Currency.from_kwargs(**currency) for currency in currencies]

    allowed_codes = [
        cur.code
        for cur in currencies
        if (cur.code.lower().startswith("usd") and cur.type == "coin")
    ]
    allowed_codes += [
        cur.code
        for cur in currencies
        if (cur.code.lower().startswith("gold"))
    ]

    currencies = [cur for cur in currencies if cur.code in allowed_codes]

    currencies.sort(key=lambda x: (x.type, x.sell, x.title))

    return currencies
