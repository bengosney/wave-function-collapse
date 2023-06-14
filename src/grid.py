# Standard Library
import random
from collections import deque
from dataclasses import dataclass

# First Party
from cell import Cell
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
        try:
            return self.cells[key]
        except KeyError:
            return self.Cell()

    def __str__(self) -> str:
        output = ""
        for y in range(self.height):
            for x in range(self.width):
                output += str(self[Vec2(x, y)])
            output += "\n"
        return output

    def _get_surrounding(self, pos: Vec2) -> list[tuple[Cell, Directions, Vec2]]:
        return [
            (self[pos + up], "up", pos + up),
            (self[pos + down], "down", pos + down),
            (self[pos + left], "left", pos + left),
            (self[pos + right], "right", pos + right),
        ]

    def collapse(self, _print=False):
        round = 0
        while not all([c.is_collapsed for c in self.cells.values()]):
            round += 1
            if round == 10:
                print(round)
            lowest = min(map(len, [c for c in self.cells.values() if not c.is_collapsed]))
            possible_next = [p for p, c in self.cells.items() if len(c) == lowest]
            start_pos = random.choice(possible_next)
            self[start_pos].pick()

            propagating = True
            while propagating:
                checked = set()
                to_check = deque([start_pos])
                propagating = False

                while len(to_check):
                    pos = to_check.pop()

                    for cell, direction, p in self._get_surrounding(pos):
                        if self[pos].collapse(cell, direction):
                            propagating = True

                        if p not in checked and self[pos].is_dirty and p in self.cells.keys() and not self[p].is_collapsed:
                            to_check.append(p)
                            checked.add(p)

                    checked.add(pos)

            if _print:
                print(self)