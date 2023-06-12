# Standard Library
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(x=self.x + other.x, y=self.y + other.y)

    def __repr__(self) -> str:
        return f"({self.x}x{self.y})"
