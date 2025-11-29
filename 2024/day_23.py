import asyncio
import sys
import pyperclip

from common import Day


class Day23(Day):
    def __init__(self):
        super().__init__(year=2024, day=23)

    computers: dict[str, set[str]] = {}

    async def part_1(self):
        async for connection in self.get_inputs():
            split = connection.split('-')
            if split[0] not in self.computers:
                self.computers[split[0]] = set()
            if split[1] not in self.computers:
                self.computers[split[1]] = set()
            self.computers[split[0]].add(split[1])
            self.computers[split[1]].add(split[0])
        trios: set[frozenset[str]] = set()
        for computer, connections in self.computers.items():
            if not computer.startswith('t'): continue
            for connection in connections:
                for connection2 in self.computers[connection]:
                    if connection2 in connections:
                        trios.add(frozenset({computer, connection, connection2}))
        return len(trios)

    def shared_connections(self, group: frozenset[str]) -> set[str]:
        intersection: set[str] | None = None
        for computer in group:
            if intersection is None:
                intersection = self.computers[computer]
            else:
                intersection = intersection.intersection(self.computers[computer])
        return intersection

    async def part_2(self):
        async for connection in self.get_inputs():
            split = connection.split('-')
            if split[0] not in self.computers:
                self.computers[split[0]] = set()
            if split[1] not in self.computers:
                self.computers[split[1]] = set()
            self.computers[split[0]].add(split[1])
            self.computers[split[1]].add(split[0])
        groups_of_n_minus_one = {frozenset({c}) for c in self.computers.keys()}
        for n in range(2, len(self.computers)):
            groups_of_n = set()
            for group in groups_of_n_minus_one:
                for computer in self.shared_connections(group):
                    groups_of_n.add(group.union({computer}))
            if len(groups_of_n) == 1:
                group, = groups_of_n
                return ','.join(sorted(group))
            groups_of_n_minus_one = groups_of_n
        raise


async def main():
    day = Day23()
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
