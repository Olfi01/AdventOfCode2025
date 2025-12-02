import asyncio
import sys
import pyperclip

from common import Day


class Day01(Day):
    def __init__(self):
        super().__init__(year=2025, day=1)

    async def part_1(self):
        pos = 50
        n = 0
        async for instruction in self.get_inputs():
            shift = int(instruction[1:]) if instruction[0] == 'R' else -int(instruction[1:])
            pos = (pos + shift) % 100
            if pos == 0: n += 1
        return n

    async def part_2(self):
        pos = 50
        n = 0
        async for instruction in self.get_inputs():
            shift = int(instruction[1:])
            for i in range(shift):
                if instruction[0] == 'R':
                    pos = (pos + 1) % 100
                else:
                    pos = (pos - 1) % 100
                if pos == 0: n += 1
        return n


async def main():
    day = Day01()
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
