# Standard Library
import random
from dataclasses import dataclass
from functools import cache

# Third Party
from rich.live import Live
from rich.text import Text

# First Party
from cell import Cell
from queue_set import Queue
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

    @staticmethod
    def _get_surrounding(pos: Vec2) -> list[tuple[Vec2, Directions]]:
        @cache
        def _surrounding() -> list[tuple[Vec2, Directions]]:
            return [
                (pos + up, "up"),
                (pos + down, "down"),
                (pos + left, "left"),
                (pos + right, "right"),
            ]

        return _surrounding()

    def collapse(self, _print=False):  # noqa: C901
        text = Text()
        with Live(text, auto_refresh=False) as live:
            while not all(c.is_collapsed for c in self.cells.values()):
                lowest = float("inf")
                possible_next = []

                for p, c in self.cells.items():
                    if not c.is_collapsed:
                        length = len(c)
                        if length < lowest:
                            lowest = length
                            possible_next = [p]
                        elif length == lowest:
                            possible_next.append(p)

                start_pos = random.choice(possible_next)
                self[start_pos].pick()

                propagating = True
                while propagating:
                    to_check = Queue([start_pos])
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
                    text.truncate(0)
                    text.append(f"{self}")
                    live.refresh()
