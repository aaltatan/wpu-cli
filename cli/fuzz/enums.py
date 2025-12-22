from enum import StrEnum


class Writer(StrEnum):
    TERMINAL = "terminal"
    FLAT_XLSX = "flat-xlsx"
    CHOICES_XLSX = "choices-xlsx"

    def __str__(self) -> str:
        return self.value


class Scorer(StrEnum):
    QUICK_RATIO = "q"
    UNICODE_QUICK_RATIO = "uq"
    WEIGHTED_RATIO = "w"
    UNICODE_WEIGHTED_RATIO = "uw"

    def __str__(self) -> str:
        return self.value


DEFAULT_PROCESSORS = [
    ("GENERAL", "general"),
    ("ARABIC", "arabic"),
]

ADDITIONAL_PROCESSORS = [
    ("WPU", "wpu"),
]

DefaultProcessor = StrEnum("DefaultProcessor", DEFAULT_PROCESSORS)
AdditionalProcessor = StrEnum("AdditionalProcessor", ADDITIONAL_PROCESSORS)
Processor = StrEnum("Processor", DEFAULT_PROCESSORS + ADDITIONAL_PROCESSORS)
