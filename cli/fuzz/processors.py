# ruff: noqa: RUF001

import re
from collections.abc import Callable
from functools import wraps

from thefuzz.utils import full_process

from .arabic import get_arabic_unicode as _
from .enums import AdditionalProcessor, DefaultProcessor, Processor

type ProcessorFn = Callable[[str], str]


_processors: dict[DefaultProcessor | AdditionalProcessor | Processor, ProcessorFn] = {}


def _get_processor_fn(processor: DefaultProcessor | AdditionalProcessor) -> ProcessorFn:
    if processor not in _processors:
        message = f"Processor '{processor}' not found"
        raise ValueError(message)

    return _processors[processor]


def get_processor_fn(processors: list[DefaultProcessor | AdditionalProcessor]) -> ProcessorFn:
    processors_functions = [_get_processor_fn(p) for p in processors]

    def wrapper(query: str) -> str:
        result = query
        for fn in processors_functions:
            result = fn(result)
        return result

    return wrapper


def register_processor(
    processor: DefaultProcessor | AdditionalProcessor | Processor,
) -> Callable[[ProcessorFn], ProcessorFn]:
    def decorator(processor_fn: ProcessorFn) -> ProcessorFn:
        @wraps(processor_fn)
        def wrapper(query: str) -> str:
            return full_process(processor_fn(query))

        _processors[processor] = wrapper
        return wrapper

    return decorator


@register_processor(Processor["GENERAL"])
def do_general_processing(query: str) -> str:
    re_replacements: list[tuple[re.Pattern, str]] = [
        (re.compile(r"\s{2,}"), ""),
    ]

    for pattern, replacement in re_replacements:
        query = re.sub(pattern, replacement, query)

    return query


@register_processor(Processor["ARABIC"])
def do_arabic_general_processing(query: str) -> str:
    re_replacements: list[tuple[re.Pattern, str]] = [
        (re.compile(rf"{_('ي')}{_('ة')}"), "يةاه"),
        (re.compile(rf"{_('ة')}(?!\w)"), "اه"),
        (re.compile(rf"{_('ظ')}"), "زظ"),
        (re.compile(rf"{_('أ')}"), "أا"),
    ]

    for pattern, replacement in re_replacements:
        query = re.sub(pattern, replacement, query)

    replacements: list[tuple[str, str]] = [
        ("ـ", ""),
    ]

    for old, new in replacements:
        query = query.replace(old, new)

    return query


@register_processor(Processor["WPU"])
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
