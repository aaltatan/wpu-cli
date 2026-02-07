from pathlib import Path

import typer


def filepath_callback(value: Path) -> Path:
    if value.exists():
        message = f"The file {value} already exists."
        raise typer.BadParameter(message)

    return value


def create_output_dir_callback(output_dir: Path) -> Path:
    if not output_dir.exists():
        output_dir.absolute().mkdir(parents=True)

    return output_dir
