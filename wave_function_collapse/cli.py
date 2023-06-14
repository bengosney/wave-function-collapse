# Third Party
import typer
from rich import print

# Locals
from .grid import Grid
from .main import tileset

app = typer.Typer()


@app.command()
def draw_grid(width: int = 40, height: int = 20, draw: bool = True):
    grid = Grid(width=width, height=height, tiles=tileset)
    grid.collapse(_print=draw)
    if not draw:
        print(str(grid))
