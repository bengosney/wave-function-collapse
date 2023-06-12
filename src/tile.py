# Standard Library
from dataclasses import dataclass
from typing import Literal

Directions = Literal["up", "down", "left", "right"]


@dataclass(frozen=True)
class Tile:
    val: str
    up: str
    down: str
    left: str
    right: str
    weight: int = 10

    def __str__(self) -> str:
        return self.val
