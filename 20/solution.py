#!/usr/bin/env python
from typing import Tuple, Dict, Set, Generator, List

Point = Tuple[int, int]


class Solver:

    def __init__(self):
        self.maze = list()
        self.start: Point | None = None
        self.end: Point | None = None
        self.width = 0
        self.height = 0

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                self.maze.append(line)
                for x, ch in enumerate(line):
                    if ch == "S":
                        self.start = (x, y)
                    elif ch == "E":
                        self.end = (x, y)
        self.height = len(self.maze)
        self.width = len(self.maze[0])

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

    def explore(self) -> Tuple[List[Point], Dict[Point, int]]:
        path: List[Point] = []
        distance: Dict[Point, int] = {}
        path.append(self.start)
        distance[self.start] = 0
        while path[-1] != self.end:
            for el in self._get_neighbours(path[-1]):
                if el in distance:
                    continue
                x, y = el
                if self.maze[y][x] != "#":
                    distance[el] = len(path)
                    path.append(el)
                    break
        return path, distance

    def _get_at_distance(self, point: Point, distance: int) -> Generator[Point, None, None]:
        x, y = point
        for dx in range(distance + 1):
            x_range = {dx, -dx}
            dy = distance - dx
            y_range = {dy, -dy}
            for delta_x in x_range:
                for delta_y in y_range:
                    yield x + delta_x, y + delta_y

    def _get_cheats_from(self, point: Point, new_rules: bool = False) -> Generator[Tuple[int, Point], None, None]:
        if new_rules:
            for target in range(2, 21):
                for x, y in self._get_at_distance(point, distance=target):
                    if 0 <= x < self.width and 0 <= y < self.height and self.maze[y][x] != "#":
                        yield target, (x, y)
        else:
            for x, y in self._get_at_distance(point, distance=2):
                if 0 <= x < self.width and 0 <= y < self.height and self.maze[y][x] != "#":
                    yield 2, (x, y)

    def solve(self, new_rules: bool = False):
        path, distance = self.explore()
        total_cost = distance[self.end]
        result = 0
        for el in path:
            current = distance[el]
            for cheat_distance, cheat in self._get_cheats_from(el, new_rules=new_rules):
                new_distance = current + cheat_distance - 1 + (len(path) - distance[cheat])
                saving = total_cost - new_distance
                if saving >= 100:
                    result += 1
        return result

    def solve1(self) -> int:
        return self.solve()

    def solve2(self) -> int:
        return self.solve(new_rules=True)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
