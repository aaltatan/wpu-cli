import typer

from rich.console import Console

from .controllers import Capacity
from .tables import table
from .utils import Wb
from ..models import Faculty, Setting

console = Console()
app = typer.Typer()


@app.command(name="list")
def list_faculties(
    locality_percentage: float | None = None,
    excel: bool = True,
):
    """
    List all faculties
    """
    locality_percentage = locality_percentage or Setting.get(key="locality_percentage")
    faculties = [
        Capacity(**faculty, locality_percentage=float(locality_percentage.value))
        for faculty in Faculty.select().dicts()
    ]
    for faculty in faculties:
        table.add_row(
            str(faculty.id),
            faculty.name,
            str(faculty.students_count),
            str(faculty.capacity),
            str(faculty.capacity_difference),
            str(faculty.required_local_count),
            str(faculty.local_count),
            str(faculty.locality_difference),
        )

    if excel:
        Wb().save_table(faculties, f"capacity-{locality_percentage}.xlsx")
        console.print(f"Excel file saved to capacity-{locality_percentage}.xlsx at your Desktop")
    else:
        console.print(table)


@app.command(name="remove")
def remove_faculty(id: int | None = None):
    """
    Remove a faculty
    """
    id = id or typer.prompt("Enter the faculty id")
    Faculty.delete_by_id(id)
    console.print("Removed successfully")


@app.command(name="add")
def add_faculty():
    """
    Add a faculty
    """
    name = typer.prompt("Enter the faculty name", type=str)
    students_count = typer.prompt("Enter the students count", type=int, default=0)
    teacher_to_student_ratio = typer.prompt(
        "Enter the teacher to student ratio",
        type=int,
        default=35,
    )
    local_fulltime_specialist_count = typer.prompt(
        "Enter the local fulltime specialist count",
        type=int,
        default=0,
    )
    foreign_fulltime_specialist_count = typer.prompt(
        "Enter the foreign fulltime specialist count",
        type=int,
        default=0,
    )

    local_fulltime_supportive_count = typer.prompt(
        "Enter the local fulltime supportive count",
        type=int,
        default=0,
    )
    foreign_fulltime_supportive_count = typer.prompt(
        "Enter the foreign fulltime supportive count",
        type=int,
        default=0,
    )
    parttime_specialist_count = typer.prompt(
        "Enter the parttime specialist count",
        type=int,
        default=0,
    )
    parttime_supportive_count = typer.prompt(
        "Enter the parttime supportive count",
        type=int,
        default=0,
    )
    master_count = typer.prompt("Enter the master count", type=int, default=0)
    Faculty.create(
        name=name,
        students_count=students_count,
        teacher_to_student_ratio=teacher_to_student_ratio,
        local_fulltime_specialist_count=local_fulltime_specialist_count,
        foreign_fulltime_specialist_count=foreign_fulltime_specialist_count,
        local_fulltime_supportive_count=local_fulltime_supportive_count,
        foreign_fulltime_supportive_count=foreign_fulltime_supportive_count,
        parttime_specialist_count=parttime_specialist_count,
        parttime_supportive_count=parttime_supportive_count,
        master_count=master_count,
    )
    console.print("Added successfully")


@app.command(name="update")
def update_faculty(id: int | None = None):
    id = id or typer.prompt("Enter the faculty id")

    faculty: Faculty = Faculty.get_by_id(id)

    name = typer.prompt("Enter the faculty name", type=str, default=faculty.name)
    students_count = typer.prompt(
        "Enter the students count", type=int, default=faculty.students_count
    )
    teacher_to_student_ratio = typer.prompt(
        "Enter the teacher to student ratio",
        type=int,
        default=faculty.teacher_to_student_ratio,
    )
    local_fulltime_specialist_count = typer.prompt(
        "Enter the local fulltime specialist count",
        type=int,
        default=faculty.local_fulltime_specialist_count,
    )
    foreign_fulltime_specialist_count = typer.prompt(
        "Enter the foreign fulltime specialist count",
        type=int,
        default=faculty.foreign_fulltime_specialist_count,
    )
    local_fulltime_supportive_count = typer.prompt(
        "Enter the local fulltime supportive count",
        type=int,
        default=faculty.local_fulltime_supportive_count,
    )
    foreign_fulltime_supportive_count = typer.prompt(
        "Enter the foreign fulltime supportive count",
        type=int,
        default=faculty.foreign_fulltime_supportive_count,
    )
    parttime_specialist_count = typer.prompt(
        "Enter the parttime specialist count",
        type=int,
        default=faculty.parttime_specialist_count,
    )
    parttime_supportive_count = typer.prompt(
        "Enter the parttime supportive count",
        type=int,
        default=faculty.parttime_supportive_count,
    )
    master_count = typer.prompt(
        "Enter the master count", type=int, default=faculty.master_count
    )

    faculty.name = name
    faculty.students_count = students_count
    faculty.teacher_to_student_ratio = teacher_to_student_ratio
    faculty.local_fulltime_specialist_count = local_fulltime_specialist_count
    faculty.local_fulltime_supportive_count = local_fulltime_supportive_count
    faculty.foreign_fulltime_specialist_count = foreign_fulltime_specialist_count
    faculty.foreign_fulltime_supportive_count = foreign_fulltime_supportive_count
    faculty.parttime_specialist_count = parttime_specialist_count
    faculty.parttime_supportive_count = parttime_supportive_count
    faculty.master_count = master_count

    faculty.save()

    console.print("Updated successfully")
