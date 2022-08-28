# Standard Library
import enum
import random
from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import Union

# Third Party
import imageio.v3 as iio
import numpy as np

img_path = Path(__file__).parent.absolute() / "images" / "plants.png"
out_path = Path(__file__).parent.absolute() / "output" / "output.png"

img = iio.imread(img_path)

OptionalPixel = Union["pixel", None]
OptionalPixels = list[OptionalPixel]


class pixel:
    class directions(enum.Enum):
        TOP = "top"
        LEFT = "left"
        RIGHT = "right"
        BOTTOM = "bottom"

    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b

        self.neighbours: dict[str, OptionalPixels] = defaultdict[str, OptionalPixels](lambda: [])

    def __iter__(self):
        yield "r", self.r
        yield "g", self.g
        yield "b", self.b

    def __str__(self) -> str:
        return f"{self.r}:{self.g}:{self.b}"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, pixel) and str(self) == str(__o)

    def __hash__(self) -> int:
        return hash(tuple(self))

    def add(self, p: OptionalPixel, direction: "directions"):
        if p is not None:
            self.neighbours[direction.name].append(p)

    @property
    def array(self):
        return [self.r, self.g, self.b]


print(img.shape)

height, width, _ = img.shape
pixels = set[pixel]()

print(height, width)

for x in range(width):
    for y in range(height):
        p = pixel(*img[x, y])
        pixels.add(p)

pixels = {str(p): p for p in pixels}
print(pixels)


def name(arr):
    return ":".join([str(c) for c in arr])


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
            cur.add(get(x, y - 1), pixel.directions.TOP)
            cur.add(get(x - 1, y), pixel.directions.LEFT)
            cur.add(get(x + 1, y), pixel.directions.RIGHT)
            cur.add(get(x, y + 1), pixel.directions.BOTTOM)

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

    top = get(x, y - 1)
    if top is not None:
        maybes.append(top.neighbours[pixel.directions.BOTTOM.name])

    left = get(x - 1, y)
    if left is not None:
        maybes.append(left.neighbours[pixel.directions.RIGHT.name])

    right = get(x + 1, y)
    if right is not None:
        maybes.append(right.neighbours[pixel.directions.LEFT.name])

    bottom = get(x, y + 1)
    if bottom is not None:
        maybes.append(bottom.neighbours[pixel.directions.TOP.name])

    def r(a, b):
        if a is None:
            return b
        if b is None:
            return []
        return [value for value in a if value in b]

    maybes = reduce(r, maybes, None)
    random.shuffle(maybes)

    print(len(set(maybes)))
    return list(set(maybes))


def solve():
    solved = False
    for x in range(gen_x):
        for y in range(gen_y):
            if name(gen[x][y]) == "0:0:0":
                maybes = possible(x, y) or []
                for p in maybes:
                    gen[x, y] = p.array
                    if not (solved := solve()):
                        gen[x, y] = [0, 0, 0]
                return solved

    return True


solve()

iio.imwrite(out_path, gen, extension=".png")
