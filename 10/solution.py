#!/usr/bin/env python
from typing import Generator, Tuple


class Solver:

    def __init__(self):
        self.data = []
        self.height = -1
        self.width = -1

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.data.append([int(x) for x in line])
        self.height = len(self.data)
        self.width = len(self.data[0])

    def _get_neighbours(self, y: int, x: int) -> Generator[Tuple[int, int], None, None]:
        if y + 1 < self.height:
            yield y + 1, x
        if y > 0:
            yield y - 1, x
        if x + 1 < self.width:
            yield y, x + 1
        if x > 0:
            yield y, x - 1

    def solve1(self) -> int:
        trail_heads = {}
        for y, line in enumerate(self.data):
            for x, char in enumerate(line):
                if char == 9:
                    trail_heads[(y, x)] = {(y, x)}
        for el in range(8, -1, -1):
            new_trail_heads = {}
            for point, reachable in trail_heads.items():
                y, x = point
                for ny, nx in self._get_neighbours(y, x):
                    if self.data[ny][nx] == el:
                        candidate = (ny, nx)
                        if candidate not in new_trail_heads:
                            new_trail_heads[candidate] = set()
                        new_trail_heads[candidate].update(reachable)
                trail_heads = new_trail_heads

        return sum([len(reachable) for reachable in trail_heads.values()])

    def solve2(self) -> int:
        trail_heads = {}
        for y, line in enumerate(self.data):
            for x, char in enumerate(line):
                if char == 9:
                    trail_heads[(y, x)] = 1
        for el in range(8, -1, -1):
            new_trail_heads = {}
            for point, reachable in trail_heads.items():
                y, x = point
                for ny, nx in self._get_neighbours(y, x):
                    if self.data[ny][nx] == el:
                        candidate = (ny, nx)
                        if candidate not in new_trail_heads:
                            new_trail_heads[candidate] = 0
                        new_trail_heads[candidate] += reachable
                trail_heads = new_trail_heads

        return sum(trail_heads.values())


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
