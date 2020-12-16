import numpy as np
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from util.progress import ChristmasProgress
console = Console()

starting_numbers = [8, 13, 1, 0, 18, 9]
turns = [2020, 30_000_000]

def play_game(starting_numbers, turns):
    s = len(starting_numbers)
    numbers = np.zeros(turns)
    numbers[:] = np.nan
    numbers[0:s] = starting_numbers
    mentions = {n: i for i, n in enumerate(starting_numbers[:-1])}
    
    with ChristmasProgress(console) as progress:
        for i in progress.track(range(s, turns)):
            prev = numbers[i-1]
            if prev not in mentions:
                numbers[i] = 0
            else:
                numbers[i] = i-1 - mentions[prev]
                mentions[prev] = i-1
            mentions[prev] = i-1
    return numbers[turns-1]

for task, turns in enumerate(turns):
    console.rule(f"Task {task + 1}")
    panel1 = Panel(
        ', '.join(str(num) for num in starting_numbers),
        title="Starting numbers",
        padding=(1, 2),
        style='blue')
    panel2 = Panel(
        Text(str(turns), justify='center'),
        title="Turns",
        padding=(1, 2),
        style='magenta')
    console.print(Columns([panel1, panel2]))

    result = play_game(starting_numbers, turns)
    panel3 = Panel.fit(
        Text(f"{result:.0f}", justify='center', style='bold'),
        title="Answer",
        padding=(1, 2),
        style='red')
    console.print(panel3)
