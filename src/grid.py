# Standard Library
import random
from dataclasses import dataclass

# First Party
from cell import Cell
from queue_set import queue
from tile import Directions, Tile
from vec2 import Vec2

up: Vec2 = Vec2(0, -1)
down: Vec2 = Vec2(0, 1)
left: Vec2 = Vec2(-1, 0)
right: Vec2 = Vec2(1, 0)


@dataclass
class Grid:
    width: int
    height: int
    tiles: list[Tile]

    def __post_init__(self):
        self.Cell = Cell.make_default(self.tiles)

        self.cells: dict[Vec2, Cell] = {}
        for x in range(self.width):
            for y in range(self.height):
                self.cells[Vec2(x, y)] = self.Cell()

    def __getitem__(self, key: Vec2) -> Cell:
        return self.cells[key]

    def __str__(self) -> str:
        output = ""
        for y in range(self.height):
            for x in range(self.width):
                output += str(self[Vec2(x, y)])
            output += "\n"
        return output

    def _get_surrounding(self, pos: Vec2) -> list[tuple[Vec2, Directions]]:
        return [
            (pos + up, "up"),
            (pos + down, "down"),
            (pos + left, "left"),
            (pos + right, "right"),
        ]

    def collapse(self, _print=False):
        while not all([c.is_collapsed for c in self.cells.values()]):
            lowest = min(map(len, [c for c in self.cells.values() if not c.is_collapsed]))
            possible_next = [p for p, c in self.cells.items() if len(c) == lowest]
            start_pos = random.choice(possible_next)
            self[start_pos].pick()

            propagating = True
            while propagating:
                to_check = queue([start_pos])
                propagating = False

                while len(to_check):
                    pos = to_check.pop()

                    for p, direction in self._get_surrounding(pos):
                        try:
                            propagating |= self[pos].collapse(self[p], direction)
                        except KeyError:
                            continue

                        if self[pos].is_dirty and not self[p].is_collapsed:
                            to_check.append(p)

            if _print:
                print(self)
