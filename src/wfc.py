# Standard Library
import enum
import random
from pathlib import Path
from typing import TypeVar, Union
from xmlrpc.client import boolean

# Third Party
import imageio.v3 as iio
import numpy as np
from rich import print
from rich.console import Console

console = Console()

img_path = Path(__file__).parent.absolute() / "images" / "plants.png"
out_path = Path(__file__).parent.absolute() / "output" / "output.png"

img = iio.imread(img_path)

OptionalPixel = Union["Pixel", None]
OptionalPixels = list[OptionalPixel]


class directions(enum.Enum):
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"


R = TypeVar("R", bound="Rule")


class Rule:
    def __init__(self, top: OptionalPixel, left: OptionalPixel, right: OptionalPixel, bottom: OptionalPixel) -> None:
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom

    def __iter__(self):
        yield self.top
        yield self.left
        yield self.right
        yield self.bottom

    def __str__(self) -> str:
        return ", ".join(
            [
                f"top: {self.top}",
                f"left: {self.left}",
                f"right: {self.right}",
                f"bottom: {self.bottom}",
            ]
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Rule) and all(
            [
                self.top == __o.top,
                self.left == __o.left,
                self.right == __o.right,
                self.bottom == __o.bottom,
            ]
        )

    def __hash__(self) -> int:
        return hash(tuple(self))

    def passes(self, x: int, y: int) -> boolean:
        return all(
            [
                self.top == get(x, y - 1),
                self.left == get(x - 1, y),
                self.right == get(x + 1, y),
                self.bottom == get(x, y + 1),
            ]
        )

    @classmethod
    def create(cls: type[R], x: int, y: int) -> R:
        return cls(get(x, y - 1), get(x - 1, y), get(x + 1, y), get(x, y + 1))


class Pixel:
    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b

        self._rules: set[Rule] = set()

    def __iter__(self):
        yield "r", self.r
        yield "g", self.g
        yield "b", self.b

    def __str__(self) -> str:
        return f"{self.r},{self.g},{self.b}"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Pixel) and str(self) == str(__o)

    def __hash__(self) -> int:
        return hash(tuple(self))

    def add_rule(self, rule: Rule):
        self._rules.add(rule)

    @property
    def rules(self):
        return list(self._rules)

    @property
    def array(self):
        return [self.r, self.g, self.b]

    @property
    def style(self):
        return f"rgb({self})"

    def print(self, end=""):
        console.print("#", style=f"rgb({self})", end=end)


print(img.shape)

height, width, _ = img.shape
pixels = set[Pixel]()

print(height, width)

for x in range(width):
    for y in range(height):
        p = Pixel(*img[x, y])
        pixels.add(p)

pixels = {str(p): p for p in pixels}
print(pixels)


def name(arr):
    return ",".join([str(c) for c in arr])


def get(x, y) -> OptionalPixel:
    if x < 0 or y < 0:
        return None
    try:
        return pixels[name(img[x, y])]
    except IndexError:
        return None


for x in range(width):
    for y in range(height):
        cur = pixels[name(img[x, y])]
        if cur is not None:
            rule = Rule.create(x, y)
            cur.add_rule(rule)

for p in pixels.values():
    p.print()
    print(f" - {len(p.rules)} rules")
print()

s = 30
gen = np.zeros([s, s, 3]).astype(np.uint8)

gen_x, gen_y, _ = gen.shape

p_list = [pixels[p] for p in pixels]

for i in range(gen_x):
    gen[0, i] = img[0, i]


def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]


def possible(x: int, y: int):
    maybes = []

    for pixel in pixels.values():
        if any([rule.passes(x, y) for rule in pixel.rules]):
            maybes.append(pixel)

    maybes = list(set(maybes))
    random.shuffle(maybes)

    for m in maybes:
        m.print()
    print(",", end="")
    return maybes


def solve():
    solved = False
    for x in range(gen_x):
        for y in range(gen_y):
            if name(gen[x][y]) == "0,0,0":
                maybes = possible(x, y) or []
                for p in maybes:
                    gen[x, y] = p.array
                    if not (solved := solve()):
                        gen[x, y] = [0, 0, 0]
                return solved

    return True


solve()

iio.imwrite(out_path, gen, extension=".png")
