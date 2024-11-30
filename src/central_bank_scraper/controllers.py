import asyncio
import itertools
from dataclasses import dataclass, field, InitVar
from datetime import datetime

import httpx
from selectolax.parser import HTMLParser


@dataclass
class ExchangeRate:
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


def parse_page(html: str) -> list[ExchangeRate]:
    parser = HTMLParser(html)
    elements = parser.css('.law > div[class^="bd"]')

    results: list[ExchangeRate] = []

    for element in elements:
        date_str = element.css_first(".w2.floatRight").text(strip=True)
        rate_str = element.css_first(".w4.floatRight").text(strip=True)
        results.append(ExchangeRate(date_str=date_str, rate_str=rate_str))

    return results


async def get_exchange_rates(pages: 1) -> list[ExchangeRate]:
    base_url = "https://cb.gov.sy/index.php?Last=3427&CurrentPage={}&First=0&page=list&ex=2&dir=exchangerate&lang=1&service=2&sorc=0&lt=0&act=1206"

    requests: list = []

    async with httpx.AsyncClient(timeout=30) as client:
        for page in range(pages):
            url = base_url.format(page)
            requests.append(client.get(url))

        results: list[ExchangeRate] = []

        batches = itertools.batched(requests, 5)

        for batch in batches:
            responses: list[httpx.Response] = await asyncio.gather(*batch)

            for response in responses:
                html = response.text
                results += parse_page(html)

            await asyncio.sleep(3)

        return results
