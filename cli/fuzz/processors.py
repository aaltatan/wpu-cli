# ruff: noqa: RUF001

import re
from collections.abc import Callable
from enum import StrEnum
from functools import wraps

from thefuzz.utils import full_process

from .arabic import get_arabic_unicode as _

type ProcessFunc = Callable[[str], str]


class Processor(StrEnum):
    GENERAL = "general"
    ARABIC = "arabic"
    WPU = "wpu"

    def __str__(self) -> str:
        return self.value


_processors: dict[Processor, ProcessFunc] = {}


def _get_processor_func(processor: Processor) -> ProcessFunc:
    if processor not in _processors:
        message = f"Processor '{processor}' not found"
        raise ValueError(message)

    return _processors[processor]


def get_processor_func(processors: list[Processor]) -> ProcessFunc:
    processors_functions = [_get_processor_func(p) for p in processors]

    def wrapper(query: str) -> str:
        result = query
        for func in processors_functions:
            result = func(result)
        return result

    return wrapper


def register_processor(
    processor: Processor,
) -> Callable[[ProcessFunc], ProcessFunc]:
    def decorator(processor_func: ProcessFunc) -> ProcessFunc:
        @wraps(processor_func)
        def wrapper(query: str) -> str:
            return full_process(processor_func(query))

        _processors[processor] = wrapper
        return wrapper

    return decorator


@register_processor(Processor.GENERAL)
def do_general_processing(query: str) -> str:
    re_replacements: list[tuple[re.Pattern, str]] = [
        (re.compile(r"\s{2,}"), ""),
    ]

    for pattern, replacement in re_replacements:
        query = re.sub(pattern, replacement, query)

    return query


@register_processor(Processor.ARABIC)
def do_arabic_general_processing(query: str) -> str:
    re_replacements: list[tuple[re.Pattern, str]] = [
        (re.compile(rf"{_('ة')}"), "هة"),
        (re.compile(rf"{_('ظ')}"), "زظ"),
        (re.compile(rf"{_('أ')}"), "أا"),
        (re.compile(rf"\b{_('ا')}{_('ل')}"), ""),
    ]

    for pattern, replacement in re_replacements:
        query = re.sub(pattern, replacement, query)

    replacements: list[tuple[str, str]] = [
        ("ـ", ""),
    ]

    for old, new in replacements:
        query = query.replace(old, new)

    return query


@register_processor(Processor.WPU)
def do_process_wpu_naming_pattern(query: str) -> str:
    replacements: dict[str, str] = {
        "أ.د.": "",
        "ا.د.": "",
        "ا.د": "",
        "أ.د": "",
        "د.": "",
    }

    for old, new in replacements.items():
        query = query.replace(old, new)

    return query
