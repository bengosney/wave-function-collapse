# Standard Library
import enum
from collections import defaultdict
from pathlib import Path
from typing import Union

# Third Party
import imageio.v3 as iio

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
        self.neighbours[direction.name].append(p)


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
    return pixels[name(img[x, y])]


for x in range(width):
    for y in range(height):
        cur = pixels[name(img[x, y])]
        if cur is not None:
            cur.add(get(x, y - 10), pixel.directions.TOP)

iio.imwrite(out_path, img, extension=".png")
