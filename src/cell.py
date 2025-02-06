import random
from dataclasses import dataclass
from functools import lru_cache, partial
from typing import Self

from tile import Directions, Tile

opposites: dict[Directions, Directions] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


@dataclass
class Cell:
    tiles: list[Tile]

    def __post_init__(self):
        self._inital_len = len(self.tiles)

    def __len__(self) -> int:
        return len(self.tiles)

    def __str__(self) -> str:
        if self.is_collapsed:
            return self.tiles[0].val
        return "*"

    def __hash__(self) -> int:
        return hash(tuple(self.tiles))

    @property
    def is_collapsed(self) -> bool:
        return len(self.tiles) == 1

    @property
    def is_dirty(self) -> bool:
        return len(self.tiles) != self._inital_len

    @lru_cache
    def get_sockets(self, direction: Directions) -> list[str]:
        return list(map(lambda t: getattr(t, direction), self.tiles))

    @lru_cache
    def other_sockets(self, direction: Directions) -> list[str]:
        return list(map(lambda s: s[::-1], self.get_sockets(opposites[direction])))

    def collapse(self, cell: Self, direction: Directions) -> bool:
        if self.is_collapsed:
            return False

        other_sockets = cell.get_sockets(opposites[direction])

        old_len = len(self.tiles)
        self.tiles = [t for t in self.tiles if getattr(t, direction) in other_sockets]
        return old_len != len(self.tiles)

    def pick(self):
        self.tiles = random.choices(self.tiles, k=1, weights=[t.weight for t in self.tiles])

    @classmethod
    def make_default(cls, tiles: list[Tile]):
        return partial(cls, tiles)
