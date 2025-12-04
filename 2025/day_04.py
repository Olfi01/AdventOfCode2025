import asyncio
import sys
import pyperclip

from common import Day


class Day04(Day):
    def __init__(self):
        super().__init__(year=2025, day=4)

    async def part_1(self):
        grid = []
        async for line in self.get_inputs():
            row = list(line)
            grid.append(row)
        n = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == '.': continue
                neighbors = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0: continue
                        if 0 <= x + dx < len(grid[y]) and 0 <= y + dy < len(grid):
                            if grid[y + dy][x + dx] == '@':
                                neighbors += 1
                if neighbors < 4:
                    n += 1
        return n

    async def part_2(self):
        grid = []
        async for line in self.get_inputs():
            row = list(line)
            grid.append(row)
        n = 0
        removed = True
        while removed:
            removed = False
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    if grid[y][x] == '.': continue
                    neighbors = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == 0 and dy == 0: continue
                            if 0 <= x + dx < len(grid[y]) and 0 <= y + dy < len(grid):
                                if grid[y + dy][x + dx] == '@':
                                    neighbors += 1
                    if neighbors < 4:
                        grid[y][x] = '.'
                        n += 1
                        removed = True
        return n


async def main():
    day = Day04()
    if len(sys.argv) > 0:
        inp = sys.argv[1]
    else:
        print('Part 1 or 2?')
        inp = input()
    res = await day.part_2() if inp == '2' else await day.part_1()
    print(res)
    pyperclip.copy(res)


if __name__ == "__main__":
    asyncio.run(main())
