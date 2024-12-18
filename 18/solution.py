#!/usr/bin/env python
from typing import Tuple, List, Set, Generator

Point = Tuple[int, int]


class Maze:

    def __init__(self, width: int, height: int, occupied: Set[Point]) -> None:
        self.width = width
        self.height = height
        self.occupied = occupied

    def _get_neighbours(self, point: Point) -> Generator[Point, None, None]:
        x, y = point
        if x > 0:
            yield x - 1, y
        if x < self.width - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < self.height - 1:
            yield x, y + 1

    def explore(self) -> int:
        maze: List[List[int | None]] = []
        for _ in range(self.height):
            maze.append([None] * self.width)

        border: Set[Point] = {(0, 0)}
        maze[0][0] = 0
        explored: Set[Point] = self.occupied.copy()
        distance = 1
        while len(border) > 0:
            new_border: Set[Point] = set()
            for el in border:
                for point in self._get_neighbours(el):
                    if point in explored:
                        continue
                    x, y = point
                    maze[y][x] = distance
                    new_border.add(point)
                explored.add(el)
            border = new_border
            distance += 1
        return maze[self.height - 1][self.width - 1]


class Solver:

    def __init__(self):
        self.positions: List[Point] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.positions.append(tuple(int(x) for x in line.split(",")))

    def solve(self, num_pixels: int) -> int | None:
        occupied = set(self.positions[:num_pixels])
        maze = Maze(71, 71, occupied)
        return maze.explore()

    def solve1(self) -> int:
        return self.solve(1024)

    def solve2(self) -> str:
        left = 0
        right = len(self.positions)
        while left < right - 1:
            mid = (right + left) // 2
            if self.solve(mid) is None:
                right = mid
            else:
                left = mid
        x, y = self.positions[left]
        return f"{x},{y}"


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %s" % solution2)


if __name__ == "__main__":
    main()
