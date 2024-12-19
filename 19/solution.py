#!/usr/bin/env python
import functools


class Solver:

    def __init__(self):
        self.patterns = []
        self.designs = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            self.patterns = hand.readline().strip().split(", ")
            hand.readline()
            for line in hand:
                self.designs.append(line.strip())

    @functools.lru_cache()
    def is_design_possible(self, design: str, start: int = 0) -> bool:
        if start == len(design):
            return True
        for pattern in self.patterns:
            end_point = start + len(pattern)
            if (
                end_point <= len(design)
                and design[start:end_point] == pattern
                and self.is_design_possible(design, end_point)
            ):
                return True
        return False

    def solve1(self) -> int:
        possible = 0
        for design in self.designs:
            if self.is_design_possible(design):
                possible += 1
        return possible

    @functools.lru_cache()
    def count_possible(self, design: str, start: int = 0) -> int:
        if start == len(design):
            return 1
        possible = 0
        for pattern in self.patterns:
            end_point = start + len(pattern)
            if end_point <= len(design) and design[start:end_point] == pattern:
                possible += self.count_possible(design, start=end_point)
        return possible

    def solve2(self) -> int:
        possible = 0
        for design in self.designs:
            possible += self.count_possible(design)
        return possible


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
