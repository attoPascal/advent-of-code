from rich.progress import *

class ChristmasProgress(Progress):
    def __init__(self, console=None):
        super().__init__(
            SpinnerColumn(spinner_name='christmas'),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=True)
