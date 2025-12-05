import asyncio
import atexit
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

from aiohttp import ClientSession

from secrets import secrets


class Day(ABC):
    def __init__(self, year: int, day: int):
        self.year: int = year
        self.day: int = day
        self.session: ClientSession = ClientSession(cookies={'session': secrets.get('SESSION_TOKEN')})
        self.testinput = False
        atexit.register(self._shutdown)

    async def get_input(self) -> str:
        if self.testinput and (test_input := self.get_testinput()) is not None:
            return test_input
        async with self.session.get(f"https://adventofcode.com/{self.year}/day/{self.day}/input") as response:
            return (await response.text()).strip()

    async def get_inputs(self, separator: str = '\n', strip: str = ' ') -> AsyncGenerator[str, Any]:
        for x in (await self.get_input()).split(separator):
            s = x.strip(strip)
            if s: yield s

    @abstractmethod
    async def part_1(self) -> Any:
        pass

    @abstractmethod
    async def part_2(self) -> Any:
        pass

    def get_testinput(self) -> str | None:
        print('Enter/Paste your test input. Ctrl-D or Ctrl-Z (on Windows) to save it.')
        contents = []
        while True:
            try:
                line = input("")
            except EOFError:
                break
            contents.append(line)
        return '\n'.join(contents)

    def _shutdown(self):
        asyncio.run(self.session.close())
