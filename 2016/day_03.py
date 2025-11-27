import asyncio
import sys
import pyperclip

from common import Day


class Day03(Day):
    def __init__(self):
        super().__init__(year=2016, day=3)

    async def part_1(self):
        n = 0
        async for triangle in self.get_inputs():
            sides = ' '.join(triangle.split()).split(' ')
            a, b, c = int(sides[0]), int(sides[1]), int(sides[2])
            if a + b > c and a + c > b and b + c > a:
                n += 1
        return n

    async def part_2(self):
        n = 0
        lines = [x async for x in self.get_inputs()]
        for i in range(0, len(lines), 3):
            sides = [list(map(int, ' '.join(l.split()).split(' '))) for l in lines[i:i+3]]
            for x in range(0, len(sides)):
                a, b, c = int(sides[0][x]), int(sides[1][x]), int(sides[2][x])
                if a + b > c and a + c > b and b + c > a:
                    n += 1
        return n


async def main():
    day = Day03()
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
