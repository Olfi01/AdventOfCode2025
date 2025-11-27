import asyncio
import re
import sys
from collections.abc import Callable

import pyperclip

from common import Day

input_regex = re.compile(r'^value (?P<value>\d+) goes to bot (?P<bot>\d+)$', re.MULTILINE)
instruction_regex = re.compile(
    r'^bot (?P<bot>\d+) gives low to (?P<typelow>output|bot) (?P<low>\d+) and high to (?P<typehigh>output|bot) (?P<high>\d+)$',
    re.MULTILINE)


class CancellationToken:
    def __init__(self):
        self._is_canceled = False

    def is_canceled(self):
        return self._is_canceled

    def cancel(self):
        self._is_canceled = True


class ChipRecipient:
    def __init__(self, _id: int):
        self.id = _id
        self.chips: list[int] = []

    async def give(self, chip: int, bots: dict, outputs: dict, cancellation_token: CancellationToken):
        self.chips.append(chip)


class Output(ChipRecipient):
    def __init__(self, _id: int):
        super().__init__(_id)


class Bot(ChipRecipient):
    def __init__(self, instruction: tuple[str, str, str, str, str], break_condition: Callable[..., bool]):
        super().__init__(int(instruction[0]))
        self.type_low = instruction[1]
        self.type_high = instruction[3]
        self.low = int(instruction[2])
        self.high = int(instruction[4])
        self.break_condition = break_condition

    async def give(self, chip: int, bots: dict[int, ChipRecipient], outputs: dict[int, Output],
                   cancellation_token: CancellationToken):
        if cancellation_token.is_canceled(): return
        if len(self.chips) > 1: raise
        await super().give(chip, bots, outputs, cancellation_token)
        if self.break_condition(self):
            cancellation_token.cancel()
            return
        if len(self.chips) == 2:
            if not self.low in outputs: outputs[self.low] = Output(self.low)
            if not self.high in outputs: outputs[self.high] = Output(self.high)
            low = outputs[self.low] if self.type_low == 'output' else bots[self.low]
            high = outputs[self.high] if self.type_high == 'output' else bots[self.high]
            async with asyncio.TaskGroup() as tg:
                tg.create_task(low.give(min(self.chips), bots, outputs, cancellation_token))
                tg.create_task(high.give(max(self.chips), bots, outputs, cancellation_token))


async def run_simulation(instructions: str, break_condition: Callable[..., bool]) -> dict[int, Output]:
    bots: dict[int, Bot] = {}
    outputs: dict[int, Output] = {}
    for instruction in instruction_regex.findall(instructions):
        bot = Bot(instruction, break_condition)
        bots[bot.id] = bot
    async with asyncio.TaskGroup() as tg:
        token = CancellationToken()
        for match in input_regex.findall(instructions):
            value, bot = int(match[0]), int(match[1])
            tg.create_task(bots[bot].give(value, bots, outputs, token))
    return outputs


class Day10(Day):
    def __init__(self):
        super().__init__(year=2016, day=10)
        self.found_bot: int | None = None

    def condition_1(self, bot: Bot) -> bool:
        if len(bot.chips) == 2 and min(bot.chips) == 17 and max(bot.chips) == 61:
            self.found_bot = bot.id
            return True
        return False

    async def part_1(self):
        instructions = await self.get_input()
        await run_simulation(instructions, self.condition_1)
        return self.found_bot

    async def part_2(self):
        instructions = await self.get_input()
        outputs = await run_simulation(instructions, lambda b: False)
        return outputs[0].chips[0] * outputs[1].chips[0] * outputs[2].chips[0]


async def main():
    day = Day10()
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
