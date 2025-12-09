from typing import Literal

import click


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
