import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli.utils import extract_extension

from .callback import app_callback
from .exporters import get_export_fn
from .options import (
    CompensationsRateOption,
    ExportPathOption,
    GrossCompensationsArgument,
    GrossSalaryArgument,
    SocialSecuritySalaryOption,
    StartAmountRangeArgument,
    StepAmountRangeArgument,
    StopAmountRangeArgument,
    TargetSalaryArgument,
)
from .services import (
    calculate_gross_taxes,
    calculate_net_salaries_from_amount_range,
    calculate_net_salary,
)
from .tables import get_salary_table

app = typer.Typer(callback=app_callback)


@app.command(name="gross")
def calculate_gross_taxes_command(
    ctx: typer.Context,
    salary: GrossSalaryArgument,
    compensations: GrossCompensationsArgument = 0,
    ss_salary: SocialSecuritySalaryOption = None,
):
    """Calculate taxes for a given gross salary and compensations."""
    _salary = calculate_gross_taxes(
        gross_salary=salary,
        gross_compensations=compensations,
        brackets=ctx.obj["brackets"],
        fixed_tax_rate=ctx.obj["fixed_tax_rate"],
        min_allowed_salary=ctx.obj["min_allowed_salary"],
        tax_rounder=ctx.obj["tax_rounder"],
        ss_obj=ctx.obj["ss"],
        ss_salary=ss_salary,
    )

    console = Console()
    table = get_salary_table(_salary, title="Gross Results")

    console.print(table)


@app.command(name="net")
def calculate_net_salary_command(
    ctx: typer.Context,
    target_salary: TargetSalaryArgument,
    compensations_rate: CompensationsRateOption,
):
    """Calculate gross salary and compensations for a given target salary."""
    salary = calculate_net_salary(
        target_salary=target_salary,
        compensations_rate=compensations_rate,
        brackets=ctx.obj["brackets"],
        fixed_tax_rate=ctx.obj["fixed_tax_rate"],
        min_allowed_salary=ctx.obj["min_allowed_salary"],
        rounder=ctx.obj["tax_rounder"],
    )

    console = Console()
    table = get_salary_table(salary, title="Net Results")

    console.print(table)


@app.command(name="ar")
def calculate_net_salaries_from_amount_range_command(  # noqa: PLR0913
    ctx: typer.Context,
    compensations_rate: CompensationsRateOption,
    start: StartAmountRangeArgument,
    stop: StopAmountRangeArgument = None,
    step: StepAmountRangeArgument = None,
    export_path: ExportPathOption = None,
):
    """Create salaries from a given amount range."""
    if stop is None:
        message = "You must provide a stop value."
        raise typer.BadParameter(message)

    if step is None:
        message = "You must provide a step value."
        raise typer.BadParameter(message)

    salaries = calculate_net_salaries_from_amount_range(
        start=start,
        stop=stop,
        step=step,
        compensations_rate=compensations_rate,
        brackets=ctx.obj["brackets"],
        min_allowed_salary=ctx.obj["min_allowed_salary"],
        fixed_tax_rate=ctx.obj["fixed_tax_rate"],
        rounder=ctx.obj["tax_rounder"],
    )

    console = Console()

    if export_path is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Exporting ... ", total=None)
            export_fn = get_export_fn(extract_extension(export_path))
            export_fn(salaries, export_path)
            console.print(f"✅ Results has been exported to {export_path}")
    else:
        table = get_salary_table(*salaries, title="Net Results")
        console.print(table)
