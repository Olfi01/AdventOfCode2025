import asyncio
import sys
import pyperclip

from common import Day


class Day03(Day):
    def __init__(self):
        super().__init__(year=2025, day=3)

    async def part_1(self):
        _sum = 0
        async for bank in self.get_inputs():
            char1 = max(bank)
            idx = bank.find(char1)
            if idx == len(bank) - 1:
                char2 = max(bank[:idx])
                _sum += int(char2 + char1)
                continue
            char2 = max(bank[idx + 1:])
            _sum += int(char1 + char2)
        return _sum

    async def part_2(self):
        _sum = 0
        async for bank in self.get_inputs():
            chars = []
            for i in range(12):
                char = max(bank[:len(bank) - (12 - i - 1)])
                idx = bank.find(char)
                bank = bank[idx + 1:]
                chars.append(char)
            _sum += int(''.join(chars))
        return _sum


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
