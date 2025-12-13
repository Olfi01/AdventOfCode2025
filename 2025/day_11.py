import asyncio
import sys
from functools import cache

import pyperclip

from common import Day


class HashableDict:
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary

    def __hash__(self):
        return hash(frozenset(self.dictionary.items()))


@cache
def number_of_paths(devices: HashableDict, start: str, end: str) -> int:
    if start == end:
        return 1
    if start not in devices.dictionary:
        return 0
    return sum(number_of_paths(devices, nxt, end) for nxt in devices.dictionary[start])


class Day11(Day):
    def __init__(self):
        super().__init__(year=2025, day=11)

    def get_testinput(self) -> str | None:
        return """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

    async def part_1(self):
        devices: dict[str, tuple[str, ...]] = dict()
        async for line in self.get_inputs():
            split = line.split(':')
            outputs = [s for s in split[1].split(' ') if s]
            devices[split[0]] = tuple(outputs)
        return number_of_paths(HashableDict(devices), 'you', 'out')

    async def part_2(self):
        devices: dict[str, tuple[str, ...]] = dict()
        async for line in self.get_inputs():
            split = line.split(':')
            outputs = [s for s in split[1].split(' ') if s]
            devices[split[0]] = tuple(outputs)
        h_devices = HashableDict(devices)
        return number_of_paths(h_devices, 'svr', 'fft') * number_of_paths(h_devices, 'fft', 'dac') * number_of_paths(
            h_devices, 'dac', 'out') + number_of_paths(h_devices, 'svr', 'dac') * number_of_paths(h_devices, 'dac',
                                                                                                  'fft') * number_of_paths(
            h_devices, 'fft', 'out')


async def main():
    day = Day11()
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
