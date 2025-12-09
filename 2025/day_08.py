import asyncio
import math
import sys
from functools import cache

import pyperclip

from common import Day


@cache
def euclidean_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2) + math.pow(a[2] - b[2], 2))


class Day08(Day):
    def __init__(self):
        super().__init__(year=2025, day=8)

    def get_testinput(self) -> str | None:
        return """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

    async def part_1(self):
        boxes = [tuple(map(lambda x: int(x), line.split(','))) async for line in self.get_inputs()]
        sets = set(map(lambda x: frozenset({x}), boxes))
        pairs = sorted({(boxes[i], boxes[j]) for i in range(len(boxes)) for j in range(i + 1, len(boxes))},
                       key=lambda x: euclidean_distance(x[0], x[1]))
        for i in range(10 if self.testinput else 1000):
            pair = pairs[i]
            found = []
            for s in sets:
                if pair[0] in s or pair[1] in s:
                    found.append(s)
            for f in found:
                sets.remove(f)
            sets.add(frozenset().union(*found))
        sets = sorted(sets, key=len, reverse=True)
        return len(sets[0]) * len(sets[1]) * len(sets[2])

    async def part_2(self):
        boxes = [tuple(map(lambda x: int(x), line.split(','))) async for line in self.get_inputs()]
        sets = set(map(lambda x: frozenset({x}), boxes))
        pairs = sorted({(boxes[i], boxes[j]) for i in range(len(boxes)) for j in range(i + 1, len(boxes))},
                       key=lambda x: euclidean_distance(x[0], x[1]))
        i = -1
        while True:
            i += 1
            pair = pairs[i]
            found = []
            for s in sets:
                if pair[0] in s or pair[1] in s:
                    found.append(s)
            for f in found:
                sets.remove(f)
            sets.add(frozenset().union(*found))
            if len(sets) == 1:
                return pair[0][0] * pair[1][0]


async def main():
    day = Day08()
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
