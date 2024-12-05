#!/usr/bin/env python
from typing import List


class Solver:

    def __init__(self):
        self.after_rules = {}
        self.orderings = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                if line == "":
                    break
                fst, snd = line.split("|", maxsplit=1)
                if fst not in self.after_rules:
                    self.after_rules[fst] = set()
                self.after_rules[fst].add(snd)
            for line in hand:
                line = line.strip()
                self.orderings.append(line.split(","))

    def _is_correct(self, ordering: List[str]) -> bool:
        N = len(ordering)
        for i, current in enumerate(ordering):
            for j in range(i + 1, N):
                after = ordering[j]
                if after in self.after_rules and current in self.after_rules[after]:
                    return False
        return True

    def solve1(self) -> int:
        total = 0
        for ordering in self.orderings:
            if self._is_correct(ordering):
                total += int(ordering[len(ordering) // 2])
        return total

    def _fix(self, ordering: List[str]) -> List[str]:
        pages = set(ordering)
        restrict = dict()
        for el in pages:
            if el in self.after_rules:
                restrict[el] = self.after_rules[el] & pages
            else:
                restrict[el] = set()
        return sorted(ordering, key=lambda page: len(restrict[page]), reverse=True)

    def solve2(self) -> int:
        total = 0
        for ordering in self.orderings:
            if not self._is_correct(ordering):
                fixed = self._fix(ordering)
                total += int(fixed[len(fixed) // 2])
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
