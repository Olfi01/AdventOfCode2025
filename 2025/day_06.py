import asyncio
import math
import sys
from itertools import product

import pyperclip

from common import Day


class Day06(Day):
    def __init__(self):
        super().__init__(year=2025, day=6)

    def get_testinput(self) -> str | None:
        return """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

    async def part_1(self):
        grid: list[list[int]] = []
        ops = []
        _sum = 0
        async for row in self.get_inputs():
            if row[0] == '*' or row[0] == '+':
                ops = [op for op in row.split(' ') if op]
                break
            grid.append([int(n) for n in row.split(' ') if n])
        for i, op in enumerate(ops):
            if op == '+':
                _sum += sum(row[i] for row in grid)
            else:
                _sum += math.prod(row[i] for row in grid)
        return _sum

    async def part_2(self):
        grid: list[list[str]] = [list(row) async for row in self.get_inputs(strip='')]
        separators = [-1]
        _sum = 0
        for i in range(max(len(row) for row in grid)):
            if not any(row[i] != ' ' for row in grid if len(row) > i):
                separators.append(i)
        for s in range(len(separators)):
            sep = separators[s]
            if s + 1 < len(separators):
                next_sep = separators[s + 1]
            else:
                next_sep = max(len(row) for row in grid)
            op = grid[-1][sep + 1]
            nums = []
            for i in range(next_sep - 1, sep, -1):
                num = 0
                for r in range(len(grid) - 1):
                    row = grid[r]
                    if i < len(row) and row[i] != ' ':
                        num = num * 10 + int(row[i])
                nums.append(num)
            if op == '+':
                _sum += sum(nums)
            else:
                _sum += math.prod(nums)
        return _sum


async def main():
    day = Day06()
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
