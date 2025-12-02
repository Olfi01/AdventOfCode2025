import asyncio
import re
import sys
import pyperclip

from common import Day

part_2_re = re.compile(r'(\d+)\1+')


class Day02(Day):
    def __init__(self):
        super().__init__(year=2025, day=2)

    async def part_1(self):
        _sum = 0
        async for _range in self.get_inputs(','):
            split = _range.split('-')
            start, end = int(split[0]), int(split[1])
            for i in range(start, end + 1):
                _id = str(i)
                length = len(_id)
                if length % 2 != 0:
                    continue
                elif _id[:length // 2] == _id[length // 2:]:
                    _sum += i
        return _sum

    async def part_2(self):
        _sum = 0
        async for _range in self.get_inputs(','):
            split = _range.split('-')
            start, end = int(split[0]), int(split[1])
            for i in range(start, end + 1):
                _id = str(i)
                if part_2_re.fullmatch(_id):
                    _sum += i
        return _sum


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
