import asyncio
import sys

from common import Day


class Day01(Day):

    def __init__(self):
        super().__init__(year=2016, day=1)

    directions = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]

    async def part_1(self) -> int:
        pos = (0,0)
        direction = 0
        async for instruction in self.get_inputs(','):
            turn = instruction[0]
            steps = int(instruction[1:])
            direction = (direction + (1 if turn == 'R' else -1)) % len(self.directions)
            pos = tuple(map(lambda x, y: x + y * steps, pos, self.directions[direction]))
        return abs(pos[0]) + abs(pos[1])

    async def part_2(self) -> int:
        pos = (0, 0)
        positions = {pos}
        direction = 0
        async for instruction in self.get_inputs(','):
            turn = instruction[0]
            steps = int(instruction[1:])
            direction = (direction + (1 if turn == 'R' else -1)) % len(self.directions)
            for i in range(0, steps):
                pos = tuple[int, int](map(lambda x, y: x + y, pos, self.directions[direction]))
                if pos in positions:
                    return abs(pos[0]) + abs(pos[1])
                positions.add(pos)
        return -1


async def main():
    day = Day01()
    if len(sys.argv) > 0:
        inp = sys.argv[1]
    else:
        print('Part 1 or 2?')
        inp = input()
    print(await day.part_2() if inp == '2' else await day.part_1())


if __name__ == "__main__":
    asyncio.run(main())
