import random
from functools import partial
from typing import Self

from tile import Directions, Tile

opposites: dict[Directions, Directions] = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class Cell:
    _tiles: list[Tile]
    _inital_len: int
    _len: int
    _is_collapsed: bool

    def __init__(self, tiles: list[Tile]):
        self.tiles = tiles
        self._inital_len = len(self.tiles)

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles

    @tiles.setter
    def tiles(self, tiles: list[Tile]):
        self._tiles = tiles
        self._len = len(tiles)
        self._is_collapsed = self._len == 1

    def __len__(self) -> int:
        return self._len

    def __str__(self) -> str:
        if self.is_collapsed:
            return self.tiles[0].val
        return "*"

    def __hash__(self) -> int:
        return hash(tuple(self.tiles))

    @property
    def is_collapsed(self) -> bool:
        return self._is_collapsed

    @property
    def is_dirty(self) -> bool:
        return self._len != self._inital_len

    def get_sockets(self, direction: Directions) -> list[str]:
        return list(map(lambda t: getattr(t, direction), self.tiles))

    def other_sockets(self, direction: Directions) -> list[str]:
        return list(map(lambda s: s[::-1], self.get_sockets(opposites[direction])))

    def collapse(self, cell: Self, direction: Directions) -> bool:
        if self.is_collapsed:
            return False

        other_sockets = cell.get_sockets(opposites[direction])

        old_len = self._len
        self.tiles = [t for t in self.tiles if getattr(t, direction) in other_sockets]
        return old_len != self._len

    def pick(self):
        self.tiles = random.choices(self.tiles, k=1, weights=[t.weight for t in self.tiles])

    @classmethod
    def make_default(cls, tiles: list[Tile]):
        return partial(cls, tiles)
