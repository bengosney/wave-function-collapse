from cProfile import Profile
from enum import Enum
from pstats import Stats

import typer

from grid import Grid
from tile import Tile


class SortType(str, Enum):
    CALLS = "calls"
    CUMULATIVE = "cumulative"
    FILENAME = "filename"
    LINE = "line"
    NAME = "name"
    NFL = "nfl"
    PCALLS = "pcalls"
    STDNAME = "stdname"
    TIME = "time"


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


def main(  # noqa: PLR0913
    progress: bool = True,
    width: int = 100,
    height: int = 40,
    full_tileset: bool = True,
    profile: bool = False,
    profile_sort: SortType = SortType.TIME,
):
    tileset = tilesets[0] + tilesets[1] if full_tileset else tilesets[0]

    grid = Grid(width=width, height=height, tiles=tileset)

    if profile:
        with Profile() as profile_output:
            grid.collapse(_print=progress)
            Stats(profile_output).strip_dirs().sort_stats(profile_sort).print_stats()
    else:
        grid.collapse(_print=progress)


def cli():
    typer.run(main)


if __name__ == "__main__":
    typer.run(main)
