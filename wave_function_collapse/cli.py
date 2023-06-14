# Third Party
import typer
from rich import print

# First Party
from wave_function_collapse.grid import Grid
from wave_function_collapse.main import tileset

app = typer.Typer()


@app.command()
def draw_grid(width: int = 40, height: int = 20, draw: bool = True):
    grid = Grid(width=width, height=height, tiles=tileset)
    grid.collapse(_print=draw)
    print(str(grid))


if __name__ == "__main__":
    draw_grid()
