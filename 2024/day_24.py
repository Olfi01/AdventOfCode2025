import asyncio
import re
import sys
from abc import ABC, abstractmethod
from asyncio import TaskGroup
from functools import cache

import pyperclip

from common import Day

input_regex = re.compile('(?P<wire>.{3}): (?P<value>[01])')
gate_spec_regex = re.compile('(?P<in1>.{3}) (?P<op>AND|OR|XOR) (?P<in2>.{3}) -> (?P<out>.{3})')


class GateLike(ABC):
    @abstractmethod
    async def set_input(self, wire: str, value: int, gates: dict[str, list]):
        pass


class Gate(GateLike):
    def __init__(self, spec: str):
        match = gate_spec_regex.match(spec)
        self.in1 = match.group('in1')
        self.op = match.group('op')
        self.in2 = match.group('in2')
        self.out = match.group('out')
        self.value1: bool | None = None
        self.value2: bool | None = None
        self.value_out: bool | None = None

    async def set_input(self, wire: str, value: bool, gates: dict[str, list[GateLike]]):
        if self.value_out is not None: return
        if wire == self.in1:
            self.value1 = value
        elif wire == self.in2:
            self.value2 = value
        else:
            raise
        if self.value1 is None or self.value2 is None: return
        if self.op == 'AND':
            self.value_out = self.value1 and self.value2
        elif self.op == 'OR':
            self.value_out = self.value1 or self.value2
        elif self.op == 'XOR':
            self.value_out = self.value1 != self.value2
        else:
            raise
        if self.out not in gates: return
        async with TaskGroup() as tg:
            for gate in gates[self.out]:
                tg.create_task(gate.set_input(self.out, self.value_out, gates))


class HashableDict:
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary

    def __hash__(self):
        return hash(frozenset(self.dictionary.items()))


async def run_simulation(gates: dict[str, list[Gate]], gates_by_output: dict[str, Gate],
                         inputs: dict[str, bool]) -> int:
    tasks = []
    for wire, value in inputs.items():
        for gate in gates[wire]:
            tasks.append(asyncio.create_task(gate.set_input(wire, value, gates)))
    await asyncio.gather(*tasks)
    if any(gate.out[0] == 'z' and gate.value_out is None for gate in gates_by_output.values()): return -1
    return sum(
        [gate.value_out * pow(2, int(gate.out[1:])) for gate in gates_by_output.values() if gate.out[0] == 'z'])


def resolve_instruction(wire: str, gates_by_output: dict[str, Gate], aliases: dict[str, str]) -> str:
    if wire in aliases: return f'{aliases[wire]}({wire})'
    if wire[0] in ['x', 'y']: return wire
    gate = gates_by_output[wire]
    return f'({resolve_instruction(gate.in1, gates_by_output, aliases)} {gate.op} {resolve_instruction(gate.in2, gates_by_output, aliases)})'


class Day24(Day):
    def __init__(self):
        super().__init__(year=2024, day=24)

    async def part_1(self):
        scanning_inputs = True
        inputs: dict[str, bool] = {}
        gates: dict[str, list[Gate]] = {}
        gates_by_output: dict[str, Gate] = {}
        async for line in self.get_inputs():
            if scanning_inputs:
                match = input_regex.match(line)
                if not match:
                    scanning_inputs = False
                else:
                    inputs[match.group('wire')] = match.group('value') == '1'
            if not scanning_inputs:
                gate = Gate(line)
                if not gate.in1 in gates:
                    gates[gate.in1] = []
                if not gate.in2 in gates:
                    gates[gate.in2] = []
                gates[gate.in1].append(gate)
                gates[gate.in2].append(gate)
                gates_by_output[gate.out] = gate
        return await run_simulation(gates, gates_by_output, inputs)

    async def part_2(self):
        scanning_inputs = True
        inputs: dict[str, bool] = {}
        gates: dict[str, list[Gate]] = {}
        gates_by_output: dict[str, Gate] = {}
        async for line in self.get_inputs():
            if scanning_inputs:
                match = input_regex.match(line)
                if not match:
                    scanning_inputs = False
                else:
                    inputs[match.group('wire')] = match.group('value') == '1'
            if not scanning_inputs:
                gate = Gate(line)
                if not gate.in1 in gates:
                    gates[gate.in1] = []
                if not gate.in2 in gates:
                    gates[gate.in2] = []
                gates[gate.in1].append(gate)
                gates[gate.in2].append(gate)
                gates_by_output[gate.out] = gate
        swapped = []
        while True:
            aliases = {}
            # ddc00: direct carry of bit 00 (x00 AND y00)
            # xor00: xor of x00, y00 (x00 XOR y00)
            # idc01: indirect carry of bit 01 (xor01 AND ddc00)
            # ccc01: carry of bit 01 (ddc01 OR idc01)
            # exp02: expected bit of result (xor02 XOR ccc01)
            for wire, gate in gates_by_output.items():
                if gate.in1[0] in ['x', 'y'] and gate.in2[0] in ['x', 'y'] and gate.in1[1:] == gate.in2[1:]:
                    if gate.op == 'AND':
                        aliases[wire] = f'ddc{gate.in1[1:]}'
                    if gate.op == 'XOR':
                        if gate.in1[1:] == '00':
                            aliases[wire] = 'exp00'
                        else:
                            aliases[wire] = f'xor{gate.in1[1:]}'
            for wire, gate in gates_by_output.items():
                if gate.in1 in aliases and gate.in2 in aliases:
                    a1, a2 = aliases[gate.in1], aliases[gate.in2]
                    if gate.op == 'AND' and a1 == 'xor01' and a2 == 'ddc00':
                        aliases[wire] = 'idc01'
                    if gate.op == 'AND' and a2 == 'xor01' and a1 == 'ddc00':
                        aliases[wire] = 'idc01'
            for wire, gate in gates_by_output.items():
                if gate.in1 in aliases and gate.in2 in aliases:
                    a1, a2 = aliases[gate.in1], aliases[gate.in2]
                    if gate.op == 'XOR' and a1 == 'xor01' and a2 == 'ddc00':
                        aliases[wire] = 'exp01'
                    if gate.op == 'XOR' and a2 == 'xor01' and a1 == 'ddc00':
                        aliases[wire] = 'exp01'
            changes = True
            while changes:
                changes = False
                for wire, gate in gates_by_output.items():
                    if wire == 'z45' and wire in aliases and aliases[wire] == 'ccc44': aliases[wire] = 'exp45'
                    if wire in aliases: continue
                    if gate.in1 in aliases and gate.in2 in aliases:
                        a1, a2 = aliases[gate.in1], aliases[gate.in2]
                        if gate.op == 'AND' and a1.startswith('xor') and a2.startswith('ccc'):
                            if int(a1[3:]) == int(a2[3:]) + 1:
                                aliases[wire] = f'idc{a1[3:]}'
                                changes = True
                        if gate.op == 'AND' and a2.startswith('xor') and a1.startswith('ccc'):
                            if int(a2[3:]) == int(a1[3:]) + 1:
                                aliases[wire] = f'idc{a2[3:]}'
                                changes = True
                        if (gate.op in ['OR', 'XOR'] and a1[:3] in ['ddc', 'idc'] and a2[:3] in ['ddc', 'idc']
                                and a1[:3] != a2[:3] and a1[3:] == a2[3:]):
                            aliases[wire] = f'ccc{a1[3:]}'
                            changes = True
                        if gate.op == 'XOR' and a1.startswith('ccc') and a2[:3].startswith('xor'):
                            if int(a1[3:]) + 1 == int(a2[3:]):
                                aliases[wire] = f'exp{a2[3:]}'
                                changes = True
                        if gate.op == 'XOR' and a2.startswith('ccc') and a1[:3].startswith('xor'):
                            if int(a2[3:]) + 1 == int(a1[3:]):
                                aliases[wire] = f'exp{a1[3:]}'
                                changes = True

            if not any(wire not in aliases or aliases[wire] != f'exp{wire[1:]}' for wire in gates_by_output.keys()
                       if wire[0] == 'z'):
                break

            print([f'z{i:02d}: ' + resolve_instruction(f'z{i:02d}', gates_by_output, aliases) for i in range(46)
                   if f'z{i:02d}' not in aliases or aliases[f'z{i:02d}'] != f'exp{i:02d}'])
            s1 = input('Choose first to swap: ')
            s2 = input('Choose second to swap: ')
            swapped += [s1, s2]
            g1 = gates_by_output[s1]
            g2 = gates_by_output[s2]
            g1.out = s2
            g2.out = s1
            gates_by_output[s1] = g2
            gates_by_output[s2] = g1
        return ','.join(sorted(swapped))


async def main():
    day = Day24()
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
