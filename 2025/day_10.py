import asyncio
import sys
from functools import cache, reduce

import ilpy
import pyperclip
from ilpy import VariableType

from common import Day


class Machine:
    def __init__(self, lights: tuple[bool, ...], buttons: tuple[tuple[int, ...], ...], joltages: tuple[int, ...]):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages


def min_light_button_presses(machine: Machine, button_index: int, lights: tuple[bool, ...]) -> int | None:
    if lights == machine.lights: return 0
    button: tuple[int, ...] = machine.buttons[button_index]
    after_press = tuple([not light if i in button else light for i, light in enumerate(lights)])
    if button_index == len(machine.buttons) - 1:
        if after_press == machine.lights:
            return 1
        else:
            return None
    else:
        dont_press = min_light_button_presses(machine, button_index + 1, lights)
        do_press = min_light_button_presses(machine, button_index + 1, after_press)
        if do_press is None:
            return dont_press
        elif dont_press is None:
            return do_press + 1
        else:
            return min(dont_press, do_press + 1)


@cache
def evaluate_min_joltage_presses(machine: Machine, maximums: tuple[int, ...], button_index,
                                 joltages: tuple[int, ...]) -> int | None:
    if joltages == machine.joltages:
        return 0
    if any(joltage > machine.joltages[i] for i, joltage in enumerate(joltages)):
        return None
    button = machine.buttons[button_index]
    if button_index == len(machine.buttons) - 1:
        for presses in range(maximums[button_index], -1, -1):
            after_presses = tuple([joltage + presses if i in button else joltage for i, joltage in enumerate(joltages)])
            if after_presses == machine.joltages:
                return presses
        return None
    else:
        min_presses = None
        for presses in range(maximums[button_index], -1, -1):
            after_presses = tuple([joltage + presses if i in button else joltage for i, joltage in enumerate(joltages)])
            if after_presses == machine.joltages:
                if min_presses is None or presses < min_presses:
                    min_presses = presses
            else:
                min_extra_presses = evaluate_min_joltage_presses(machine, maximums, button_index + 1, after_presses)
                if min_extra_presses is not None:
                    if min_presses is None or min_extra_presses + presses < min_presses:
                        min_presses = min_extra_presses + presses
        return min_presses


def min_joltage_button_presses(machine: Machine):
    objective = ilpy.Variable('x0', index=0)
    for i in range(len(machine.buttons)):
        objective += ilpy.Variable('x' + str(i), index=i)
    objective = objective.as_objective(ilpy.Sense.Minimize)
    constraints = [
                      (reduce(lambda a, b: a + b,
                              [ilpy.Variable('x' + str(i), index=i) for i, button in enumerate(machine.buttons) if
                               row in button]) == joltage).as_constraint()
                      for row, joltage
                      in enumerate(machine.joltages)] + [(ilpy.Variable('x' + str(i), index=i) >= 0).as_constraint() for
                                                         i in range(len(machine.buttons))]
    solution = ilpy.solve(objective, constraints, variable_type=VariableType.Integer)
    return int(sum(solution.variable_values))


class Day10(Day):
    def __init__(self):
        super().__init__(year=2025, day=10)

    def get_testinput(self) -> str | None:
        return """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    async def part_1(self):
        machines: list[Machine] = []
        async for line in self.get_inputs():
            split = line.split(' ')
            lights = tuple([c == '#' for c in split[0][1:-1]])
            joltages = tuple([int(i) for i in split[-1][1:-1].split(',')])
            buttons = tuple([tuple(map(int, chunk[1:-1].split(','))) for chunk in split[1:-1]])
            machines.append(Machine(lights, buttons, joltages))
        n = 0
        for machine in machines:
            presses = min_light_button_presses(machine, 0, tuple([False] * len(machine.lights)))
            if presses is None: raise RuntimeError
            n += presses
        return n

    async def part_2(self):
        machines: list[Machine] = []
        async for line in self.get_inputs():
            split = line.split(' ')
            lights = tuple([c == '#' for c in split[0][1:-1]])
            joltages = tuple([int(i) for i in split[-1][1:-1].split(',')])
            buttons = tuple([tuple(map(int, chunk[1:-1].split(','))) for chunk in split[1:-1]])
            machines.append(Machine(lights, buttons, joltages))
        n = 0
        for i, machine in enumerate(machines):
            presses = min_joltage_button_presses(machine)
            n += presses
        return n


async def main():
    day = Day10()
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
