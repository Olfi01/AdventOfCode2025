import asyncio
import re
import sys
from functools import cmp_to_key

import pyperclip

from common import Day


class Day04(Day):
    def __init__(self):
        super().__init__(year=2016, day=4)

    async def part_1(self) -> int:
        _sum = 0
        async for line in self.get_inputs():
            room = Room(line)
            if room.is_real():
                _sum += room.sector
        return _sum

    async def part_2(self) -> int:
        async for line in self.get_inputs():
            room = Room(line)
            if room.is_real():
                print(f"{room.decrypt_name()}: {room.sector}")
        return 0


room_regex = re.compile('(?P<name>[a-z\\-]+)-(?P<sector>\\d+)\\[(?P<checksum>[a-z]{5})]')


class Room:
    def __init__(self, line):
        match = room_regex.match(line)
        self.name = match.group('name')
        self.sector = int(match.group('sector'))
        self.checksum = match.group('checksum')

    def is_real(self) -> bool:
        return self.checksum == self.check_sum()

    def check_sum(self) -> str:
        chars = set(self.name)
        chars.remove('-')
        sort = sorted(chars, key=cmp_to_key(self.compare))
        return ''.join(sort[:5])

    def compare(self, x: str, y: str) -> int:
        count_x, count_y = self.name.count(x), self.name.count(y)
        if count_x < count_y:
            return 1
        elif count_x > count_y:
            return -1
        return ord(x) - ord(y)

    def decrypt_name(self) -> str:
        shift = self.sector % 26
        s = ''
        for c in self.name:
            if c == '-':
                s += ' '
            else:
                i = ord(c) + shift
                if i > 97 + 25: i -= 26
                s += chr(i)
        return s

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
