import asyncio
import re
import sys
import pyperclip
from colorama import Back

from common import Day


class Day08(Day):
    def __init__(self):
        super().__init__(year=2016, day=8)

    screen = [[False for x in range(50)] for y in range(6)]

    def perform_instruction(self, instruction: str):
        if match := rect_regex.match(instruction):
            a, b = int(match.group('A')), int(match.group('B'))
            for x in range(a):
                for y in range(b):
                    self.screen[y][x] = True
        elif match := rotate_row_regex.match(instruction):
            a, b = int(match.group('A')), int(match.group('B'))
            row = self.screen[a]
            new_row = [row[(x - b) % 50] for x in range(50)]
            self.screen[a] = new_row
        elif match := rotate_column_regex.match(instruction):
            a, b = int(match.group('A')), int(match.group('B'))
            new_column = [self.screen[(y - b) % 6][a] for y in range(6)]
            for y in range(6):
                self.screen[y][a] = new_column[y]
        else:
            raise

    def print_screen(self):
        print()
        for row in self.screen:
            print(''.join(map(lambda b: Back.GREEN + ' ' if b else Back.RESET + ' ', row)))
        print()


    async def part_1(self):
        async for instruction in self.get_inputs():
            self.perform_instruction(instruction)
        return sum(x.count(True) for x in self.screen)

    async def part_2(self):
        async for instruction in self.get_inputs():
            self.perform_instruction(instruction)
        self.print_screen()
        return 'read it yourself you lazy bum'


rect_regex = re.compile(r'rect (?P<A>\d+)x(?P<B>\d+)')
rotate_row_regex = re.compile(r'rotate row y=(?P<A>\d+) by (?P<B>\d+)')
rotate_column_regex = re.compile(r'rotate column x=(?P<A>\d+) by (?P<B>\d+)')


async def main():
    day = Day08()
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
