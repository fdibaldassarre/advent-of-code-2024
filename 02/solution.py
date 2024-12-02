#!/usr/bin/env python
from typing import List


def sgn(a: int) -> int:
    if a == 0:
        return 0
    return 1 if a > 0 else -1


class Solver:

    def __init__(self):
        self.data = list()

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.data.append([int(el) for el in line.split()])

    def is_safe(self, report: List[int]) -> bool:
        dir = sgn(report[1] - report[0])
        if dir == 0:
            return False
        is_safe = True
        for i in range(len(report) - 1):
            delta = report[i + 1] - report[i]
            if sgn(delta) != dir or abs(delta) < 1 or abs(delta) > 3:
                is_safe = False
                break
        return is_safe

    def solve1(self) -> int:
        safe = 0
        for report in self.data:
            if self.is_safe(report):
                safe += 1
        return safe

    def solve2(self) -> int:
        safe = 0
        for report in self.data:
            for i in range(len(report)):
                new_report = [el for el in report]
                del new_report[i]
                if self.is_safe(new_report):
                    safe += 1
                    break
        return safe


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
