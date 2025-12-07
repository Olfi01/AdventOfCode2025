import asyncio
import sys
from functools import cache

import pyperclip

from common import Day


def count_splits(grid: list[list[str]], startpos: tuple[int, int], visited: set[tuple[int, int]]) -> int:
    if startpos in visited or not (0 <= startpos[0] < len(grid[0])):
        return 0
    visited.add(startpos)
    x, y = startpos[0], startpos[1] + 1
    while y < len(grid):
        if (x, y) in visited:
            return 0
        visited.add((x, y))
        c = grid[y][x]
        if c == '^':
            return 1 + count_splits(grid, (x - 1, y), visited) + count_splits(grid, (x + 1, y), visited)
        y += 1
    return 0


@cache
def count_quantum_splits(grid: tuple[tuple[str, ...], ...], startpos: tuple[int, int]) -> int:
    if not (0 <= startpos[0] < len(grid[0])):
        return 0
    x, y = startpos[0], startpos[1] + 1
    while y < len(grid):
        c = grid[y][x]
        if c == '^':
            return 1 + count_quantum_splits(grid, (x - 1, y)) + count_quantum_splits(grid, (x + 1, y))
        y += 1
    return 0


class Day07(Day):
    def __init__(self):
        super().__init__(year=2025, day=7)

    def get_testinput(self) -> str | None:
        return """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

    async def part_1(self):
        grid = [list(row) async for row in self.get_inputs()]
        startpos = (-1, -1)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 'S':
                    startpos = (x, y)
        return count_splits(grid, startpos, set())

    async def part_2(self):
        grid = [list(row) async for row in self.get_inputs()]
        startpos = (-1, -1)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 'S':
                    startpos = (x, y)
        return 1 + count_quantum_splits(tuple([tuple(row) for row in grid]), startpos)


async def main():
    day = Day07()
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    else:
        print('Part 1 or 2?')
        inp = input()
    if len(sys.argv) > 2:
        day.testinput = not not sys.argv[2]
    res = await day.part_2() if inp == '2' else await day.part_1()
    print(res)
    pyperclip.copy(res)


if __name__ == "__main__":
    asyncio.run(main())
