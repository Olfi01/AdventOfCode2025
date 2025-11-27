import asyncio
import regex as re
import sys
import pyperclip

from common import Day


class Day07(Day):
    def __init__(self):
        super().__init__(year=2016, day=7)

    async def part_1(self):
        n = 0
        async for address in self.get_inputs():
            if supports_tls(address): n += 1
        return n

    async def part_2(self):
        n = 0
        async for address in self.get_inputs():
            if supports_ssl(address): n += 1
        return n


supernet_regex = re.compile(r'(?:^|(?<=]))[^\[]+(?:(?=\[)|$)')
hypernet_regex = re.compile(r'(?<=\[)[^]]+(?=])')
abba_regex = re.compile(r'(\w)(?!\1)(\w)\2\1')
aba_regex = re.compile(r'(\w)(?!\1)(\w)\1')


def supports_tls(address: str) -> bool:
    hypernet_matches = hypernet_regex.findall(address)
    if any(abba_regex.search(match) for match in hypernet_matches): return False
    supernet_matches = supernet_regex.findall(address)
    return any(abba_regex.search(match) for match in supernet_matches)


def supports_ssl(address: str) -> bool:
    supernet_matches = supernet_regex.findall(address)
    babs = [x[1] + x[0] + x[1] for match in supernet_matches for x in aba_regex.findall(match, overlapped=True) if x]
    return any(bab in match for match in hypernet_regex.findall(address) for bab in babs)


async def main():
    day = Day07()
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
