# Standard Library
import pathlib
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import product

# Third Party
from icecream import ic
from PIL import Image

block_size = 2


@dataclass(frozen=True)
class Tile:
    val: object
    up: str
    down: str
    left: str
    right: str
    weight: int = 10
    size: int = block_size


cwd = pathlib.Path(__file__).parent
img_path = cwd / "plant.png"
img = Image.open(img_path)
img = img.convert("RGB")
w, h = img.size

grid = product(range(0, h - h % block_size, block_size), range(0, w - w % block_size, block_size))


def rgb_to_str(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"{r}:{g}:{b}"


tiles: set[Tile] = set()


def pixels_to_list(pixels) -> Iterable[int]:
    for x in range(block_size):
        for y in range(block_size):
            yield pixels[x, y]


for y, x in grid:
    box = (x, y, x + block_size, y + block_size)
    part = img.crop(box)
    tile = Tile(
        val=tuple(pixels_to_list(part.load())),
        up="|".join(map(rgb_to_str, [part.getpixel((x, 0)) for x in range(block_size)])),
        down="|".join(map(rgb_to_str, [part.getpixel((x, block_size - 1)) for x in range(block_size)])),
        left="|".join(map(rgb_to_str, [part.getpixel((0, y)) for y in range(block_size)])),
        right="|".join(map(rgb_to_str, [part.getpixel((block_size - 1, y)) for y in range(block_size)])),
    )

    tiles.add(tile)

ic(tiles)
print(len(tiles))
