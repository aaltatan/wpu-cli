from pathlib import Path
from typing import Literal

import click
from playwright.sync_api import Page


def raise_missing_option_exception(
    param_type: Literal["option", "argument"],
    param_name: str,
    param_shortname: str | None = None,
    message: str | None = None,
) -> None:
    if param_shortname is not None and param_type == "argument":
        message = f"Cannot specify short name for argument '{param_name}'"
        raise ValueError(message)

    if param_type == "option":
        param_name = f"--{param_name}"

    param_hint = param_name

    if param_shortname:
        param_hint = f"-{param_shortname} / --{param_name}"

    raise click.MissingParameter(
        param_type=param_type,
        param_hint=param_hint,
        message=message,
    )


def get_authenticated_page(p, username: str, password: str) -> Page:
    browser = p.chromium.launch(slow_mo=10, headless=False)
    page = browser.new_page()
    page.goto("http://edu/")

    page.wait_for_timeout(2_000)
    page.click("#login")

    page.fill('input[name="user_id"]', username)
    page.fill("#password", password)
    page.click('button[type="submit"]')

    page.wait_for_timeout(10_000)

    return page


def get_salaries_filepath() -> Path:
    home = Path.cwd().home()
    desktop_path = home / "Desktop"
    onedrive_path = Path("D:\\OneDrive\\wpu\\salaries\\in-progress")

    glob = list(desktop_path.glob("[Salaries|Partial]*.xlsb"))

    if len(glob) > 0:
        filepath = glob[0]
    else:
        glob = list(onedrive_path.glob("[Salaries|Partial]*.xlsb"))
        filepath = glob[0]

    return filepath
