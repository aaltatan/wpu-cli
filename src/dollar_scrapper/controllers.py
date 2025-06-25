import asyncio
import itertools

import httpx
from selectolax.parser import HTMLParser

from .schemas import CentralBankExchangeRate, DollarLiraCurrency, SpTodayExchangeRate


def parse_sp_today_page(html: str) -> list[SpTodayExchangeRate]:
    parser = HTMLParser(html)

    rows = parser.css("table.local-cur > tbody > tr")

    results: list[SpTodayExchangeRate] = []

    for row in rows:
        currency = row.css_first("th a span:first-of-type").text(strip=True)
        currency_symbol = (
            row.css_first("th a span.cur-ramz strong")
            .text(strip=True)
            .replace("(", "")
            .replace(")", "")
        )
        purchase = row.css_first("td strong").text(strip=True)
        sale = row.css_first("td:nth-of-type(3) strong").text(strip=True)
        results.append(
            SpTodayExchangeRate(
                currency=currency,
                currency_symbol=currency_symbol,
                purchase=purchase,
                sale=sale,
            )
        )

    return results


def get_sp_today_exchange_rates(url: str) -> list[SpTodayExchangeRate]:
    response = httpx.get(url)
    return parse_sp_today_page(response.text)


def get_dollar_lira_exchange_rates(url: str) -> list[DollarLiraCurrency]:
    response = httpx.get(url)

    data: dict = response.json()

    currencies = data.get("currencies", [])
    currencies = [DollarLiraCurrency.from_kwargs(**currency) for currency in currencies]

    allowed_codes = [
        cur.code
        for cur in currencies
        if (cur.code.lower().startswith("usd") and cur.type == "coin")
    ]
    allowed_codes += [
        cur.code for cur in currencies if (cur.code.lower().startswith("gold"))
    ]

    currencies = [cur for cur in currencies if cur.code in allowed_codes]

    currencies.sort(key=lambda x: (x.type, x.sell, x.title))

    return currencies


def parse_central_bank_page(html: str) -> list[CentralBankExchangeRate]:
    parser = HTMLParser(html)

    selector_root: str = "div[class^=bd]:not(:first-of-type)"

    dates = parser.css(f"{selector_root} > div:first-of-type")
    rates = parser.css(f"{selector_root} > div:nth-of-type(2)")

    results: list[CentralBankExchangeRate] = []

    for date, rate in zip(dates, rates):
        date_str = date.text(strip=True)
        rate_str = rate.text(strip=True)
        results.append(CentralBankExchangeRate(date_str=date_str, rate_str=rate_str))

    return results


async def get_central_bank_exchange_rates(
    url: str,
    pages: int = 1,
) -> list[CentralBankExchangeRate]:
    requests: list = []

    async with httpx.AsyncClient(timeout=30) as client:
        for page in range(pages):
            url = url.format(page)
            requests.append(client.get(url))

        results: list[CentralBankExchangeRate] = []

        batches = itertools.batched(requests, 5)

        for batch in batches:
            responses: list[httpx.Response] = await asyncio.gather(*batch)

            for response in responses:
                html = response.text
                results += parse_central_bank_page(html)

            await asyncio.sleep(3)

        return results
