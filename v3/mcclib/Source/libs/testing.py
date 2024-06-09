import time
from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn,Console

class dummy():
    def write(*args):pass
    def flush(*args):pass

console = Console(file=dummy(),quiet=False,no_color=False,record=True)


with Progress(console=console,redirect_stdout=False) as progress:

    task1 = progress.add_task("[red]Downloading...", total=1000)
    task2 = progress.add_task("[green]Processing...", total=1000)
    task3 = progress.add_task("[cyan]Cooking...", total=1000)

    try:
        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.9)
            print( progress.console._record_buffer )
            time.sleep(0.02)
    except KeyboardInterrupt: pass