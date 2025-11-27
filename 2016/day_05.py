import asyncio
import sys
from hashlib import md5

import pyperclip

from common import Day


class Day05(Day):
    def __init__(self):
        super().__init__(year=2016, day=5)

    async def part_1(self):
        door_id = await self.get_input()
        password = ''
        i = 0
        while len(password) < 8:
            s = door_id + str(i)
            h = md5(s.encode()).hexdigest()
            if h[:5] == '00000':
                password += h[5]
            i += 1
        return password

    async def part_2(self):
        door_id = await self.get_input()
        password = '________'
        print(password, end='\r', flush=True)
        i = 0
        while '_' in password:
            s = door_id + str(i)
            h = md5(s.encode()).hexdigest()
            if h[:5] == '00000':
                pos = h[5]
                if pos.isdigit() and int(pos) < len(password) and password[int(pos)] == '_':
                    password = password[:int(pos)] + h[6] + password[int(pos) + 1:]
                    print(password, end='\r', flush=True)
            i += 1
        return password


async def main():
    day = Day05()
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
