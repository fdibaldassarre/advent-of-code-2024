#!/usr/bin/env python
import abc
import functools
from typing import List, Tuple, Dict, Set, Generator

Point = Tuple[int, int]
Move = str
NUMERIC_KEY_PAD = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
DIRECTIONAL_KEY_PAD = [
    [None, "^", "A"],
    ["<", "v", ">"],
]

MOVES = {"<": (-1, 0), "^": (0, -1), ">": (1, 0), "v": (0, 1)}


def vector_sum(point: Point, direction: Tuple[int, int]) -> Point:
    return point[0] + direction[0], point[1] + direction[1]


class Pad:

    def __init__(self, grid: List[List[str]]) -> None:
        self.grid = grid
        self.grid_height = len(grid)
        self.grid_width = len(grid[0])
        self.btn_to_position: Dict[str, Point] = {}
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch is not None:
                    self.btn_to_position[ch] = (x, y)

    def _is_valid(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height and self.grid[y][x] is not None

    def _get_neighbours(self, point: Point) -> Generator[Tuple[Point, Move], None, None]:
        for move, direction in MOVES.items():
            neighbour = vector_sum(point, direction)
            if self._is_valid(neighbour):
                yield neighbour, move

    def get_paths_between(self, start: str, end: str) -> Set[str]:
        start_pos = self.btn_to_position[start]
        end_pos = self.btn_to_position[end]
        paths: Dict[Point, Set[str]] = {start_pos: {""}}
        border: Set[Point] = {start_pos}
        explored: Set[Point] = set()
        while end_pos not in border:
            new_border: Set[Point] = set()
            for point in border:
                for neighbour, move in self._get_neighbours(point):
                    if neighbour in explored:
                        continue
                    new_border.add(neighbour)
                    if neighbour not in paths:
                        paths[neighbour] = set()
                    for point_moves in paths[point]:
                        paths[neighbour].add(point_moves + move)
                explored.add(point)
            border = new_border
        return paths[end_pos]


class Writer:
    def get_min_moves_to_write(self, code: str) -> int:
        raise NotImplementedError("")


class Human(Writer):
    def get_min_moves_to_write(self, code: str) -> int:
        return len(code)


class Robot(Writer):
    def __init__(self, pad: Pad, parent: Writer) -> None:
        self.pad = pad
        self.parent = parent

    @functools.lru_cache()
    def get_min_moves_to_write(self, code: str) -> int:
        current = "A"
        min_moves = 0
        for ch in code:
            possible_paths = self.pad.get_paths_between(current, ch)
            possible_costs = []
            for possible_path in possible_paths:
                path_cost = self.parent.get_min_moves_to_write(possible_path + "A")
                possible_costs.append(path_cost)
            min_moves += min(possible_costs)
            current = ch
        return min_moves


class Solver:

    def __init__(self):
        self.codes: List[str] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                self.codes.append(line.strip())

    def get_robot(self, num_directional: int = 2) -> Robot:
        numeric_pad = Pad(NUMERIC_KEY_PAD)
        direction_pad = Pad(DIRECTIONAL_KEY_PAD)
        human = Human()
        controller = human
        for _ in range(num_directional):
            controller = Robot(direction_pad, controller)
        return Robot(numeric_pad, controller)

    def solve(self, num_directional: int = 2) -> int:
        robot_numeric = self.get_robot(num_directional=num_directional)

        result = 0
        for code in self.codes:

            cost = robot_numeric.get_min_moves_to_write(code)

            code_num = int(code[:-1])
            result += code_num * cost

        return result

    def solve1(self) -> int:
        return self.solve(num_directional=2)

    def solve2(self) -> int:
        return self.solve(num_directional=25)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
