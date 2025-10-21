import os

import httpx
from dotenv import load_dotenv

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
    end: int = 100,
    step: int = 1,
) -> list[Salary]:
    """
    generate salaries by rate range
    """
    data = {"amount": amount, "start": start, "end": end, "step": step}

    if tax_id is not None:
        data["taxId"] = tax_id

    response = httpx.get(TAXES_ENDPOINT + "rate-sequence-generator", params=data)

    if response.status_code in [404, 422]:
        raise ValueError(
            "❌ "
            + str(response.status_code)
            + " - "
            + response.json()["detail"][0]["msg"]
        )

    return Salary.from_bulk_response(response.json())
