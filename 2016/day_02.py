import asyncio
import sys

import pyperclip

from common import Day


class Day02(Day):
    def __init__(self):
        super().__init__(year=2016, day=2)

    keypad_1 = [[x + 3 * y for x in range(1, 4)] for y in range(0, 3)]

    async def part_1(self) -> str:
        code = ''
        x, y = 1, 1
        async for instructions in self.get_inputs():
            for instruction in instructions:
                x = max(0, x - 1) if instruction == 'L' else min(2, x + 1) if instruction == 'R' else x
                y = max(0, y - 1) if instruction == 'U' else min(2, y + 1) if instruction == 'D' else y
            code += str(self.keypad_1[y][x])
        return code

    keypad_2 = [
        [' ', ' ', '1', ' ', ' '],
        [' ', '2', '3', '4', ' '],
        ['5', '6', '7', '8', '9'],
        [' ', 'A', 'B', 'C', ' '],
        [' ', ' ', 'D', ' ', ' ']
    ]

    async def part_2(self):
        code = ''
        x, y = 0, 2
        async for instructions in self.get_inputs():
            for instruction in instructions:
                new_x = max(0, x - 1) if instruction == 'L' else min(4, x + 1) if instruction == 'R' else x
                new_y = max(0, y - 1) if instruction == 'U' else min(4, y + 1) if instruction == 'D' else y
                if self.keypad_2[new_y][new_x] != ' ':
                    x, y = new_x, new_y
            code += self.keypad_2[y][x]
        return code


async def main():
    day = Day02()
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
