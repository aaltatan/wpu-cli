from enum import StrEnum


class Chapter(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"

    def __str__(self) -> str:
        return self.value
