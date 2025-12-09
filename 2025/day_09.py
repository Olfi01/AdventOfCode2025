import asyncio
import sys
import turtle
from functools import cache

import png
import pyperclip
from first import first

from common import Day


class HashableDict:
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary

    def __hash__(self):
        return hash(frozenset(self.dictionary.items()))


@cache
def area(rect: tuple[tuple[int, int], tuple[int, int]]) -> int:
    a = rect[0]
    b = rect[1]
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)


@cache
def within_edge(edge: tuple[tuple[int, int], tuple[int, int]], x: int, y: int):
    from_x, to_x = sorted([edge[0][0], edge[1][0]])
    from_y, to_y = sorted([edge[0][1], edge[1][1]])
    return from_x <= x <= to_x and from_y <= y <= to_y


@cache
def get_corner_type(horizontal_edge: tuple[tuple[int, int], tuple[int, int]] | None,
                    vertical_edge: tuple[tuple[int, int], tuple[int, int]] | None) -> str | None:
    if (not horizontal_edge) or (not vertical_edge): return None
    horizontal_goes_right = vertical_edge[0][0] == min(horizontal_edge[0][0], horizontal_edge[1][0])
    vertical_goes_up = horizontal_edge[0][1] == max(vertical_edge[0][1], vertical_edge[1][1])
    if horizontal_goes_right:
        if vertical_goes_up:
            return 'L'
        else:
            return 'F'
    else:
        if vertical_goes_up:
            return 'J'
        else:
            return '7'


manual_cache = {}


@cache
def is_green_or_red(x: int, y: int, horizontal_edges: HashableDict,
                    vertical_edges: HashableDict, min_x: int, min_y: int):
    if (any(within_edge(edge, x, y) for edge in horizontal_edges.dictionary.get(y, [])) or
            any(within_edge(edge, x, y) for edge in vertical_edges.dictionary.get(x, []))):
        return True
    if (x, y) in manual_cache: return manual_cache[(x, y)]
    inside = False
    if x - min_x < y - min_y:
        jump_start = min_x
        for i in range(x - 1, min_x, -1):
            if (i, y) in manual_cache:
                jump_start = i
                inside = manual_cache[(i, y)]
                break
        iterator = iter(range(jump_start, x))
        for i in iterator:
            vertical_edge = first(edge for edge in vertical_edges.dictionary.get(i, []) if within_edge(edge, i, y))
            if vertical_edge:
                horizontal_edge = first(
                    edge for edge in horizontal_edges.dictionary.get(y, []) if within_edge(edge, i, y))
                if horizontal_edge:
                    corner_type = get_corner_type(horizontal_edge, vertical_edge)
                    jump_to = max(horizontal_edge[0][0], horizontal_edge[1][0])
                    for j in range(i, jump_to):
                        next(iterator)
                    next_corner_type = get_corner_type(horizontal_edge, first(
                        edge for edge in vertical_edges.dictionary.get(jump_to, []) if within_edge(edge, jump_to, y)))
                    if corner_type == 'L' and next_corner_type == '7':
                        inside = not inside
                    elif corner_type == 'F' and next_corner_type == 'J':
                        inside = not inside
                else:
                    inside = not inside
            else:
                manual_cache[(i, y)] = inside
    else:
        jump_start = min_y
        for i in range(y - 1, min_y, -1):
            if (x, i) in manual_cache:
                jump_start = i
                inside = manual_cache[(x, i)]
                break
        iterator = iter(range(jump_start, y))
        for i in iterator:
            horizontal_edge = first(edge for edge in horizontal_edges.dictionary.get(i, []) if within_edge(edge, x, i))
            if horizontal_edge:
                vertical_edge = first(
                    edge for edge in vertical_edges.dictionary.get(x, []) if within_edge(edge, x, i))
                if vertical_edge:
                    corner_type = get_corner_type(horizontal_edge, vertical_edge)
                    jump_to = max(vertical_edge[0][1], vertical_edge[1][1])
                    for j in range(i, jump_to):
                        next(iterator)
                    next_corner_type = get_corner_type(
                        first(edge for edge in horizontal_edges.dictionary.get(jump_to, []) if
                              within_edge(edge, x, jump_to)), vertical_edge)
                    if corner_type == 'F' and next_corner_type == 'J':
                        inside = not inside
                    elif corner_type == '7' and next_corner_type == 'L':
                        inside = not inside
                else:
                    inside = not inside
            else:
                manual_cache[(x, i)] = inside
    return inside


def all_green_or_red(rect: tuple[tuple[int, int], tuple[int, int]],
                     horizontal_edges: HashableDict,
                     vertical_edges: HashableDict, min_x: int,
                     min_y: int) -> bool:
    left, right = sorted([rect[0][0], rect[1][0]])
    top, bottom = sorted([rect[0][1], rect[1][1]])
    if not is_green_or_red(left, top, horizontal_edges, vertical_edges, min_x, min_y):
        return False
    if not is_green_or_red(left, bottom, horizontal_edges, vertical_edges, min_x, min_y):
        return False
    if not is_green_or_red(right, top, horizontal_edges, vertical_edges, min_x, min_y):
        return False
    if not is_green_or_red(right, bottom, horizontal_edges, vertical_edges, min_x, min_y):
        return False
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            if not is_green_or_red(x, y, horizontal_edges, vertical_edges, min_x, min_y):
                return False
    return True


@cache
def crosses_vertical_edge(y: int, left: int, right: int, vertical_edges: HashableDict) -> bool:
    for x in range(left + 1, right):
        edges = vertical_edges.dictionary.get(x)
        if edges and any(within_edge(edge, x, y) and edge[0] != (x, y) and edge[1] != (x, y) for edge in edges):
            return True
    return False


@cache
def crosses_horizontal_edge(x: int, top: int, bottom: int, horizontal_edges: HashableDict) -> bool:
    for y in range(top + 1, bottom):
        edges = horizontal_edges.dictionary.get(y)
        if edges and any(within_edge(edge, x, y) for edge in edges):
            return True
    return False


@cache
def crosses_any_edge(rect: tuple[tuple[int, int], tuple[int, int]],
                     horizontal_edges: HashableDict,
                     vertical_edges: HashableDict) -> bool:
    left = min(rect[0][0], rect[1][0])
    top = min(rect[0][1], rect[1][1])
    right = max(rect[0][0], rect[1][0])
    bottom = max(rect[0][1], rect[1][1])
    if crosses_vertical_edge(top, left, right, vertical_edges):
        return True
    if crosses_vertical_edge(bottom, left, right, vertical_edges):
        return True
    if crosses_horizontal_edge(left, top, bottom, horizontal_edges):
        return True
    if crosses_horizontal_edge(right, top, bottom, horizontal_edges):
        return True
    return False


def mismatching_corners(rect: tuple[tuple[int, int], tuple[int, int]], horizontal_edges: HashableDict,
                        vertical_edges: HashableDict) -> bool:
    left = min(rect[0][0], rect[1][0])
    top = min(rect[0][1], rect[1][1])
    right = max(rect[0][0], rect[1][0])
    bottom = max(rect[0][1], rect[1][1])
    top_horizontal = {(left, top), (right, top)}
    bottom_horizontal = {(left, bottom), (right, bottom)}
    left_vertical = {(left, top), (left, bottom)}
    right_vertical = {(right, top), (right, bottom)}

    tl_horizontal = first(
        edge for edge in horizontal_edges.dictionary.get(top, []) if edge[0][0] == left or edge[1][0] == left)
    tl_vertical = first(
        edge for edge in vertical_edges.dictionary.get(left, []) if edge[0][1] == top or edge[1][1] == top)
    top_left = get_corner_type(tl_horizontal, tl_vertical)
    if top_left and set(tl_horizontal) == top_horizontal and set(tl_vertical) == left_vertical and top_left != 'F':
        return True

    tr_horizontal = first(
        edge for edge in horizontal_edges.dictionary.get(top, []) if edge[0][0] == right or edge[1][0] == right)
    tr_vertical = first(
        edge for edge in vertical_edges.dictionary.get(right, []) if edge[0][1] == top or edge[1][1] == top)
    top_right = get_corner_type(tr_horizontal, tr_vertical)
    if top_right and set(tr_horizontal) == top_horizontal and set(tr_vertical) == right_vertical and top_right != '7':
        return True

    bl_horizontal = first(
        edge for edge in horizontal_edges.dictionary.get(bottom, []) if edge[0][0] == left or edge[1][0] == left)
    bl_vertical = first(
        edge for edge in vertical_edges.dictionary.get(left, []) if edge[0][1] == bottom or edge[1][1] == bottom)
    bottom_left = get_corner_type(bl_horizontal, bl_vertical)
    if bottom_left and set(bl_horizontal) == bottom_horizontal and set(
            bl_vertical) == left_vertical and bottom_left != 'L':
        return True

    br_horizontal = first(
        edge for edge in horizontal_edges.dictionary.get(bottom, []) if edge[0][0] == right or edge[1][0] == right)
    br_vertical = first(
        edge for edge in vertical_edges.dictionary.get(right, []) if edge[0][1] == bottom or edge[1][1] == bottom)
    bottom_right = get_corner_type(br_horizontal, br_vertical)
    if bottom_right and set(br_horizontal) == bottom_horizontal and set(
            br_vertical) == right_vertical and bottom_right != 'J':
        return True

    return False


def draw(corners: list[tuple[int, ...]], rect: tuple[tuple[int, int], tuple[int, int]]) -> None:
    turtle.clear()
    turtle.penup()
    turtle.home()
    turtle.pendown()
    turtle.color('black')
    factor = 0.005
    turtle.hideturtle()
    turtle.delay(0)
    for i in range(-1, len(corners) - 1):
        start = corners[i]
        end = corners[i + 1]
        if end[0] > start[0]:
            turtle.forward((end[0] - start[0]) * factor)
        elif end[0] < start[0]:
            turtle.left(180)
            turtle.forward((start[0] - end[0]) * factor)
            turtle.right(180)
        elif end[1] > start[1]:
            turtle.right(90)
            turtle.forward((end[1] - start[1]) * factor)
            turtle.left(90)
        elif end[1] < start[1]:
            turtle.left(90)
            turtle.forward((start[1] - end[1]) * factor)
            turtle.right(90)
    root = corners[-1]
    left = min(rect[0][0], rect[1][0])
    top = min(rect[0][1], rect[1][1])
    right = max(rect[0][0], rect[1][0])
    bottom = max(rect[0][1], rect[1][1])
    pos = (left - root[0], top - root[1])
    turtle.penup()
    turtle.goto(pos[0] * factor, pos[1] * factor * -1)
    turtle.pendown()
    turtle.color('red')
    turtle.forward((right - left) * factor)
    turtle.right(90)
    turtle.forward((bottom - top) * factor)
    turtle.right(90)
    turtle.forward((right - left) * factor)
    turtle.right(90)
    turtle.forward((bottom - top) * factor)
    turtle.right(90)


class Day09(Day):
    def __init__(self):
        super().__init__(year=2025, day=9)

    def get_testinput(self) -> str | None:
        return """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    async def part_1(self):
        corners = [tuple(map(int, line.split(','))) async for line in self.get_inputs()]
        rects = sorted([(corners[i], corners[j]) for i in range(len(corners)) for j in range(i + 1, len(corners))],
                       key=area, reverse=True)
        return area(rects[0])

    async def part_2(self):
        corners = [tuple(map(int, line.split(','))) async for line in self.get_inputs()]
        min_x, min_y = min(corner[0] for corner in corners), min(corner[1] for corner in corners)
        edges = frozenset({(corners[i], corners[i + 1]) for i in range(-1, len(corners) - 1)})
        horizontal_edges = {}
        for edge in edges:
            if edge[0][1] == edge[1][1]:
                horizontal_edges[edge[0][1]] = horizontal_edges.get(edge[0][1], frozenset()).union(frozenset({edge}))
        vertical_edges = {}
        for edge in edges:
            if edge[0][0] == edge[1][0]:
                vertical_edges[edge[0][0]] = vertical_edges.get(edge[0][0], frozenset()).union(frozenset({edge}))
        rects = sorted([(corners[i], corners[j]) for i in range(len(corners)) for j in range(i + 1, len(corners))],
                       key=area, reverse=True)
        print(f'{len(rects)} rectangles to search')
        i = 35672  # first fallback: 35673
        while True:
            i += 1
            if i % 100 == 0:
                print(i)
            rect = rects[i]
            # if (94543, 48498) not in rect:
            #     continue
            if (94543, 50265) not in rect:
                continue
            # if i < 34000: continue
            if crosses_any_edge(rect, HashableDict(horizontal_edges), HashableDict(vertical_edges)):
                continue
            # if mismatching_corners(rect, HashableDict(horizontal_edges), HashableDict(vertical_edges)):
            #     continue
            print(f'Fallback reached: {i}')
            print(area(rect))
            draw(corners, rect)
            input()
            if all_green_or_red(rect, HashableDict(horizontal_edges), HashableDict(vertical_edges), min_x, min_y):
                return area(rect)


async def main():
    day = Day09()
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
