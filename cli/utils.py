from pathlib import Path


def extract_extension(path: Path) -> str:
    return path.suffix.lower().replace(".", "")
