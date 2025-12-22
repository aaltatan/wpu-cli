from typing import Annotated

import typer

PDFOpt = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Generate a PDF file(s)",
        rich_help_panel="PDF",
        expose_value=True,
    ),
]
