import asyncio
import sys
import pyperclip

from common import Day


class Day05(Day):
    def __init__(self):
        super().__init__(year=2025, day=5)

    def get_testinput(self) -> str | None:
        return super().get_testinput()

    async def part_1(self):
        blocks = [block async for block in self.get_inputs('\n\n')]
        ranges = []
        for line in blocks[0].split('\n'):
            split = line.split('-')
            ranges.append((int(split[0]), int(split[1])))
        n = 0
        for line in blocks[1].split('\n'):
            _id = int(line)
            if any(r[0] <= _id <= r[1] for r in ranges):
                n += 1
        return n

    async def part_2(self):
        blocks = [block async for block in self.get_inputs('\n\n')]
        ranges = []
        for line in blocks[0].split('\n'):
            split = line.split('-')
            ranges.append((int(split[0]), int(split[1])))
        ranges_counted = []
        for r in ranges:
            to_remove = []
            for rc in ranges_counted:
                if rc[0] <= r[0] <= rc[1]:
                    r = (rc[1] + 1, r[1])
                if rc[0] <= r[1] <= rc[1]:
                    r = (r[0], rc[0] - 1)
                if r[0] <= rc[0] <= rc[1] <= r[1]:
                    to_remove.append(rc)
            for remove in to_remove:
                ranges_counted.remove(remove)
            if r[1] >= r[0]:
                ranges_counted.append(r)
        return sum((r[1] - r[0] + 1) for r in ranges_counted)


async def main():
    day = Day05()
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
