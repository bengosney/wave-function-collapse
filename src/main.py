# Standard Library
import random

# First Party
from grid import Grid
from tile import Tile

random.seed(1)

tileset = [
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
    Tile(" ", up="aaa", right="aaa", down="aaa", left="aaa", weight=100),
]

grid = Grid(width=40, height=20, tiles=tileset)
grid.collapse(_print=True)

print("=" * 40)
print(grid)
