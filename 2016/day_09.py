import asyncio
import re
import sys
from functools import cache

import pyperclip

from common import Day


class Day09(Day):
    def __init__(self):
        super().__init__(year=2016, day=9)

    async def part_1(self):
        file = await self.get_input()
        result = decompress(file)
        return len(result)

    async def part_2(self):
        file = await self.get_input()
        length = decompressed_length(file)
        return length


marker_regex = re.compile(r'\((?P<length>\d+)x(?P<n>\d+)\)')


def decompress(file: str) -> str:
    result = ''
    i = 0
    while i < len(file):
        match = marker_regex.search(file, i)
        if match:
            result += file[i:match.start()]
            length, n = int(match.group('length')), int(match.group('n'))
            next_index = match.end()
            capture = file[next_index:next_index + length]
            result += capture * n
            i = next_index + length
        else:
            result += file[i:]
            break
    return result


@cache
def decompressed_length(file: str) -> int:
    _sum = 0
    i = 0
    while i < len(file):
        match = marker_regex.search(file, i)
        if match:
            _sum += match.start() - i
            length, n = int(match.group('length')), int(match.group('n'))
            next_index = match.end()
            capture_length = decompressed_length(file[next_index:next_index + length])
            _sum += capture_length * n
            i = next_index + length
        else:
            _sum += len(file) - i
            break
    return _sum


async def main():
    day = Day09()
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
