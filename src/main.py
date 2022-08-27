# Standard Library
from random import shuffle

grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class sudoku:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    def __str__(self) -> str:
        return "\n".join([" ".join(str(col) for col in row) for row in self.grid])

    @staticmethod
    def _rand_range(start: int, end: int):
        numbers = list(range(start, end))
        shuffle(numbers)
        while len(numbers):
            yield numbers.pop()

    def _possible(self, y: int, x: int, n: int) -> bool:
        for i in range(0, 9):
            if self.grid[y][i] == n:
                return False
        for i in range(0, 9):
            if self.grid[i][x] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0 + i][x0 + j] == n:
                    return False
        return True

    def solve(self) -> bool:
        solved = False
        for y in range(9):
            for x in range(9):
                if self.grid[y][x] == 0:
                    for n in self._rand_range(1, 10):
                        if self._possible(y, x, n):
                            self.grid[y][x] = n
                            if not (solved := self.solve()):
                                self.grid[y][x] = 0
                    return solved

        return True


if __name__ == "__main__":
    s = sudoku(grid)
    print(s)
    s.solve()
    print()
    print(s)
