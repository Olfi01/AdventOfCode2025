import asyncio
import sys
import pyperclip

from common import Day


class Day06(Day):
    def __init__(self):
        super().__init__(year=2016, day=6)

    async def part_1(self):
        frequencies = []
        async for message in self.get_inputs():
            for i in range(0, len(message)):
                char = message[i]
                if len(frequencies) <= i: frequencies.append({})
                if char not in frequencies[i]: frequencies[i][char] = 0
                frequencies[i][char] += 1
        s = ''
        for freq in frequencies:
            s += max(freq, key=freq.get)
        return s

    async def part_2(self):
        frequencies = []
        async for message in self.get_inputs():
            for i in range(0, len(message)):
                char = message[i]
                if len(frequencies) <= i: frequencies.append({})
                if char not in frequencies[i]: frequencies[i][char] = 0
                frequencies[i][char] += 1
        s = ''
        for freq in frequencies:
            s += min(freq, key=freq.get)
        return s


async def main():
    day = Day06()
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
