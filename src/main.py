# Third Party
import typer

# First Party
from grid import Grid
from tile import Tile

tilesets = [
    [
        Tile("═", up="aaa", right="aba", down="aaa", left="aba"),
        Tile("║", up="aba", right="aaa", down="aba", left="aaa"),
        Tile("╔", up="aaa", right="aba", down="aba", left="aaa"),
        Tile("╚", up="aba", right="aba", down="aaa", left="aaa"),
        Tile("╗", up="aaa", right="aaa", down="aba", left="aba"),
        Tile("╝", up="aba", right="aaa", down="aaa", left="aba"),
        Tile("╬", up="aba", right="aba", down="aba", left="aba"),
        Tile("╠", up="aba", right="aba", down="aba", left="aaa"),
        Tile("╣", up="aba", right="aaa", down="aba", left="aba"),
        Tile("╦", up="aaa", right="aba", down="aba", left="aba"),
        Tile("╩", up="aba", right="aba", down="aaa", left="aba"),
        Tile(" ", up="aaa", right="aaa", down="aaa", left="aaa", weight=1000),
        Tile("🯅", up="aaa", right="aaa", down="aaa", left="aaa", weight=1),
    ],
    [
        Tile("─", up="aaa", right="aca", down="aaa", left="aca"),
        Tile("│", up="aca", right="aaa", down="aca", left="aaa"),
        Tile("┌", up="aaa", right="aca", down="aca", left="aaa"),
        Tile("└", up="aca", right="aca", down="aaa", left="aaa"),
        Tile("┐", up="aaa", right="aaa", down="aca", left="aca"),
        Tile("┘", up="aca", right="aaa", down="aaa", left="aca"),
        Tile("┼", up="aca", right="aca", down="aca", left="aca"),
        Tile("├", up="aca", right="aca", down="aca", left="aaa"),
        Tile("┤", up="aca", right="aaa", down="aca", left="aca"),
        Tile("┬", up="aaa", right="aca", down="aca", left="aca"),
        Tile("┴", up="aca", right="aca", down="aaa", left="aca"),
        Tile("╤", up="aaa", right="aba", down="aca", left="aba"),
        Tile("╧", up="aca", right="aba", down="aaa", left="aba"),
        Tile("╟", up="aba", right="aca", down="aba", left="aaa"),
        Tile("╢", up="aba", right="aaa", down="aba", left="aca"),
        Tile("╥", up="aaa", right="aca", down="aba", left="aca"),
        Tile("╨", up="aba", right="aca", down="aaa", left="aca"),
        Tile("╞", up="aca", right="aba", down="aca", left="aaa"),
        Tile("╡", up="aca", right="aaa", down="aca", left="aba"),
    ],
]


def main(progress: bool = True, width: int = 100, height: int = 40, full_tileset: bool = True):
    tileset = tilesets[0] + tilesets[1] if full_tileset else tilesets[0]

    grid = Grid(width=width, height=height, tiles=tileset)
    grid.collapse(_print=progress)


if __name__ == "__main__":
    typer.run(main)
