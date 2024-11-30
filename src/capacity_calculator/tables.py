from rich.table import Table

table = Table(show_header=True, header_style="bold magenta")

table.add_column("#", style="blue", justify="right")
table.add_column("name", style="white", justify="right")
table.add_column("students", style="white", justify="right")
table.add_column("capacity", style="white", justify="right")
table.add_column("capacity diff", style="white", justify="right")
table.add_column("required local", style="white", justify="right")
table.add_column("local", style="white", justify="right")
table.add_column("locality diff", style="white", justify="right")