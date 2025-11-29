import asyncio
import sys
import pyperclip

from common import Day


def overlap(lock: list[int], key: list[int]) -> bool:
    for a, b in zip(lock, key):
        if a + b > 5:
            return True
    return False


class Day25(Day):
    def __init__(self):
        super().__init__(year=2024, day=25)

    async def part_1(self):
        locks = []
        keys = []
        async for block in self.get_inputs('\n\n'):
            if block.startswith('#'):
                heights = [0] * 5
                for line in block.splitlines()[1:]:
                    for i in range(5):
                        if line[i] == '#': heights[i] += 1
                locks.append(heights)
            if block.startswith('.'):
                heights = [0] * 5
                for line in block.splitlines()[:6]:
                    for i in range(5):
                        if line[i] == '#': heights[i] += 1
                keys.append(heights)
        n = 0
        for lock in locks:
            for key in keys:
                if not overlap(lock, key):
                    n += 1
        return n

    async def part_2(self):
        return 0


async def main():
    day = Day25()
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
