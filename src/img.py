# Standard Library
import pathlib
from dataclasses import dataclass
from itertools import product

# Third Party
from PIL import Image

block_size = 12


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

print(img_path)


def rgb_to_str(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"{r}:{g}:{b}"


tiles = []

for y, x in grid:
    print(f"{x} x {y}")
    box = (x, y, x + block_size, y + block_size)
    part = img.crop(box)
    tile = Tile(
        val=part,
        up="|".join(map(rgb_to_str, [part.getpixel((x, 0)) for x in range(block_size)])),
        down="|".join(map(rgb_to_str, [part.getpixel((x, block_size - 1)) for x in range(block_size)])),
        left="|".join(map(rgb_to_str, [part.getpixel((0, y)) for y in range(block_size)])),
        right="|".join(map(rgb_to_str, [part.getpixel((block_size - 1, y)) for y in range(block_size)])),
    )

    tiles.append(tile)
