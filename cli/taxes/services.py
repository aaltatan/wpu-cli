import os

import httpx
from dotenv import load_dotenv

from .exceptions import NotFoundError, ServerError
from .schemas import Salary

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL") or ""
API_VERSION = os.getenv("API_VERSION") or ""
TAXES_ENDPOINT = (
    API_BASE_URL + f"v{API_VERSION}" + "/financial/salaries-calculator/"
)


def calculate_net_salary(
    gross_salary: float,
    compensations: float | None = None,
    tax_id: int | None = None,
    ss_salary: int | None = None,
    ss_id: int | None = None,
) -> Salary:
    data = {"grossSalary": gross_salary}

    if compensations is not None:
        data["compensations"] = compensations

    if tax_id is not None:
        data["taxId"] = tax_id

    if ss_salary is not None:
        data["socialSecuritySalary"] = ss_salary

    if ss_id is not None:
        data["socialSecurityId"] = ss_id

    response = httpx.get(TAXES_ENDPOINT, params=data)

    if response.status_code in [404, 422]:
        raise ValueError(
            "❌ "
            + str(response.status_code)
            + " - "
            + response.json()["detail"][0]["msg"]
        )

    return Salary.from_response(response.json())


def calculate_gross_salary(
    amount: float,
    compensations_rate: float | None = None,
    tax_id: int | None = None,
    ss_salary: int | None = None,
    ss_id: int | None = None,
) -> Salary:
    data = {"amount": amount}

    if compensations_rate is not None:
        data["compensationsRate"] = compensations_rate

    if tax_id is not None:
        data["taxId"] = tax_id

    if ss_salary is not None:
        data["socialSecuritySalary"] = ss_salary

    if ss_id is not None:
        data["socialSecurityId"] = ss_id

    response = httpx.get(TAXES_ENDPOINT + "generator", params=data)

    if response.status_code in [404, 422]:
        raise ValueError(
            "❌ "
            + str(response.status_code)
            + " - "
            + response.json()["detail"][0]["msg"]
        )

    return Salary.from_response(response.json())


def generate_salaries_by_rate_range(
    amount: float,
    tax_id: int | None = None,
    start: int = 0,
    stop: int = 100,
    step: int = 1,
) -> list[Salary]:
    data = {"amount": amount, "start": start, "stop": stop, "step": step}

    if tax_id is not None:
        data["taxId"] = tax_id

    response = httpx.get(TAXES_ENDPOINT + "rate-range-generator", params=data)

    if response.status_code == httpx.codes.BAD_REQUEST:
        message = "❌ 500 - Server error"
        raise ServerError(message)

    if response.status_code == httpx.codes.NOT_FOUND:
        message = "❌ 404 - " + response.json()["detail"][0]["msg"]
        raise NotFoundError(message)

    if response.status_code == httpx.codes.UNPROCESSABLE_ENTITY:
        message = "❌ 422 - " + response.json()["detail"][0]["msg"]
        raise ValueError(message)

    return Salary.from_bulk_response(response.json())


def generate_salaries_by_amount_range(
    compensations_rate: float,
    start: int,
    stop: int | None = None,
    step: int | None = None,
    tax_id: int | None = None,
) -> list[Salary]:
    data = {"compensationsRate": compensations_rate, "start": start}

    if stop is not None:
        data["stop"] = stop

    if step is not None:
        data["step"] = step

    if tax_id is not None:
        data["taxId"] = tax_id

    response = httpx.get(TAXES_ENDPOINT + "amount-range-generator", params=data)

    if response.status_code == httpx.codes.BAD_REQUEST:
        message = "❌ 500 - Server error"
        raise ServerError(message)

    if response.status_code == httpx.codes.NOT_FOUND:
        message = "❌ 404 - " + response.json()["detail"][0]["msg"]
        raise NotFoundError(message)

    if response.status_code == httpx.codes.UNPROCESSABLE_ENTITY:
        message = "❌ 422 - " + response.json()["detail"][0]["msg"]
        raise ValueError(message)

    return Salary.from_bulk_response(response.json())
