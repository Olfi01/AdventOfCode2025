#if ($aoc_day.length() < 2)
#set ($aoc_fday = '0' + $aoc_day)
#else
#set ($aoc_fday = $aoc_day)
#end
import asyncio
import sys
import pyperclip

from common import Day

class Day${aoc_fday}(Day):
    def __init__(self):
        super().__init__(year=${aoc_year}, day=${aoc_day.replaceFirst("^0+(?!$)", "")})

    def get_testinput(self) -> str | None:
        return super().get_testinput()
        
    async def part_1(self):
        return 0
    
    async def part_2(self):
        return 0
       
async def main():
    day = Day${aoc_fday}()
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