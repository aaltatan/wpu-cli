import os

import httpx
from dotenv import load_dotenv

from .exceptions import NotFoundError, ServerError
from .schemas import Salary

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TAXES_ENDPOINT = BASE_URL + "financial/salaries-calculator/"


def calculate_salary(
    gross_salary: int,
    compensations: int | None = None,
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


def generate_salary(
    amount: int,
    compensations_rate: int | None = None,
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
    amount: int,
    tax_id: int | None = None,
    start: int = 0,
    stop: int = 100,
    step: int = 1,
) -> list[Salary]:
    data = {"amount": amount, "start": start, "stop": stop, "step": step}

    if tax_id is not None:
        data["taxId"] = tax_id

    response = httpx.get(TAXES_ENDPOINT + "rate-sequence-generator", params=data)

    if response.status_code == 500:
        raise ServerError("❌ 500 - Server error")

    if response.status_code == 404:
        raise NotFoundError("❌ 404 - " + response.json()["detail"][0]["msg"])

    if response.status_code == 422:
        raise ValueError("❌ 422 - " + response.json()["detail"][0]["msg"])

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

    response = httpx.get(TAXES_ENDPOINT + "amount-sequence-generator", params=data)

    if response.status_code == 500:
        raise ServerError("❌ 500 - Server error")

    if response.status_code == 404:
        raise NotFoundError("❌ 404 - " + response.json()["detail"][0]["msg"])

    if response.status_code == 422:
        raise ValueError("❌ 422 - " + response.json()["detail"][0]["msg"])

    return Salary.from_bulk_response(response.json())
