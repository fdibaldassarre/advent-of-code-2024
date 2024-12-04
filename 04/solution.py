#!/usr/bin/env python
from typing import List, Iterable

DIRECTIONS = [
    (1, 0), (-1, 0),
    (0, 1), (0, -1),
    (1, 1), (-1, -1),
    (-1, 1), (1, -1)
]

DIAGONALS = [
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
]


def vector_sum(v: Iterable[int], d: Iterable[int]) -> List[int]:
    res = []
    for x, delta in zip(v, d):
        res.append(x + delta)
    return res


class Solver:

    def __init__(self):
        self.data = []
        self.width = -1
        self.height = -1

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                self.data.append(line.strip())
        self.width = len(self.data[0])
        self.height = len(self.data)

    def _in_range(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _find_xmas_at(self, x: int, y: int) -> int:
        n_found = 0
        for direction in DIRECTIONS:
            dx, dy = direction
            found = True
            for pos, ch in enumerate("XMAS"):
                cx, cy = x + pos * dx, y + pos * dy
                if not self._in_range(cx, cy):
                    found = False
                    break
                if self.data[cy][cx] != ch:
                    found = False
                    break
            if found:
                n_found += 1
        return n_found

    def _get_data_at(self, x: int, y: int) -> int | None:
        if not self._in_range(x, y):
            return None
        return self.data[y][x]

    def _has_xmas_at(self, x: int, y: int) -> bool:
        if self.data[y][x] != "A":
            return False
        for diagonal in DIAGONALS:
            m1x, m1y = diagonal
            m2x, m2y = m1y, -1 * m1x
            s1x, s1y = -1 * m1x, -1 * m1y
            s2x, s2y = -1 * m2x, -1 * m2y
            m1x, m1y = vector_sum((x, y), (m1x, m1y))
            m2x, m2y = vector_sum((x, y), (m2x, m2y))
            s1x, s1y = vector_sum((x, y), (s1x, s1y))
            s2x, s2y = vector_sum((x, y), (s2x, s2y))

            if self._get_data_at(m1x, m1y) == "M" and self._get_data_at(m2x, m2y) == "M" and \
               self._get_data_at(s1x, s1y) == "S" and self._get_data_at(s2x, s2y) == "S":
                return True
        return False

    def solve1(self) -> int:
        total = 0
        for x in range(self.width):
            for y in range(self.height):
                total += self._find_xmas_at(x, y)
        return total

    def solve2(self) -> int:
        total = 0
        for x in range(self.width):
            for y in range(self.height):
                if self._has_xmas_at(x, y):
                    total += 1
        return total


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
