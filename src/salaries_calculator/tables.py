from rich.table import Table

table = Table()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Gross salary", style="white", justify="right")
table.add_column("Compensations", style="white", justify="right")
table.add_column("Total salary", style="blue", justify="right")
table.add_column("SS deduction", style="white", justify="right")
table.add_column("Layers tax", style="white", justify="right")
table.add_column("Fixed tax", style="white", justify="right")
table.add_column("Total deductions", style="blue", justify="right")
table.add_column("Net salary", style="white", justify="right")
table.add_column("Compensations rate", style="white", justify="right")