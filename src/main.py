# Standard Library
import random
from dataclasses import dataclass, field
from typing import Literal, Self

# Third Party
from PIL import Image

# First Party
from img import Tile, block_size, tiles

Directions = Literal["up", "down", "left", "right"]
Vec2 = tuple[int, int]

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def add_vec(a: Vec2, b: Vec2) -> Vec2:
    x1, y1 = a
    x2, y2 = b

    return (x1 + x2, y1 + y2)


opposites: dict[Directions, Directions] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


def makeTiles():
    return tiles.copy()


@dataclass
class Cell:
    tiles: list[Tile] = field(default_factory=makeTiles)

    def __post_init__(self):
        self._inital_len = len(self.tiles)

    def __len__(self) -> int:
        return len(self.tiles)

    def __str__(self) -> str:
        if self.is_collapsed:
            return "*"
        else:
            count = len(self.tiles)
            if count >= 10:
                return "+"
            return f"{count}"

    @property
    def is_collapsed(self) -> bool:
        return len(self.tiles) == 1

    @property
    def is_dirty(self) -> bool:
        return len(self.tiles) != self._inital_len

    def get_sockets(self, direction: Directions) -> list[str]:
        return list(map(lambda t: getattr(t, direction), self.tiles))

    def collapse(self, cell: Self, direction: Directions) -> bool:
        if self.is_collapsed:
            return False

        other_sockets = list(map(lambda s: s[::-1], cell.get_sockets(opposites[direction])))
        other_sockets = list(map(lambda s: s, cell.get_sockets(opposites[direction])))

        old_len = len(self.tiles)
        self.tiles = [t for t in self.tiles if getattr(t, direction) in other_sockets]
        return old_len != len(self.tiles)

    def pick(self):
        # ic([t.weight for t in self.tiles])
        # ic(self.tiles)
        self.tiles = random.choices(self.tiles, k=1, weights=[t.weight for t in self.tiles])


random.seed(1)

tile_count = len(makeTiles())
grid_size_y = 20
grid_size_x = 20
grid: dict[Vec2, Cell] = {}

for y in range(grid_size_y):
    for x in range(grid_size_x):
        grid[(x, y)] = Cell()


def rand_pos():
    return (random.randint(0, grid_size_x - 1), random.randint(0, grid_size_y - 1))


def print_grid():
    print()
    for y in range(grid_size_y):
        print()
        for x in range(grid_size_x):
            print(grid[(x, y)], end="")


empty_cell = Cell()


def get_cell(pos: Vec2) -> Cell:
    try:
        return grid[pos]
    except KeyError:
        return Cell()


def get_surrounding(pos) -> list[tuple[Cell, Directions]]:
    return [
        (get_cell(add_vec(pos, up)), "up"),
        (get_cell(add_vec(pos, down)), "down"),
        (get_cell(add_vec(pos, left)), "left"),
        (get_cell(add_vec(pos, right)), "right"),
    ]


while not all([c.is_collapsed for c in grid.values()]):
    possibilities = sum(map(len, grid)) - (grid_size_x * grid_size_y)

    lowest = min(map(len, [c for c in grid.values() if not c.is_collapsed]))
    possible_next = [p for p, c in grid.items() if len(c) == lowest]
    pos = random.choice(possible_next)
    grid[pos].pick()

    propagating = True
    while propagating:
        propagating = False
        for y in range(grid_size_y):
            for x in range(grid_size_x):
                pos = (x, y)

                if grid[pos].is_collapsed:
                    continue

                for cell, direction in get_surrounding(pos):
                    if cell.is_dirty:
                        propagating |= grid[pos].collapse(cell, direction)

    print_grid()


output = Image.new("RGB", (grid_size_x * block_size, grid_size_y * block_size))
for y in range(grid_size_y):
    for x in range(grid_size_x):
        pass

output.save("output.png")
