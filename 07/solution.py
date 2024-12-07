#!/usr/bin/env python
from typing import List, Tuple

Equation = Tuple[int, List[int]]


class Solver:

    def __init__(self):
        self.equations: List[Equation] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                result, values = line.split(": ", maxsplit=1)
                values_int = [int(value) for value in values.split(" ")]
                self.equations.append((int(result), values_int))

    def _is_valid(self, equation: Equation, additional_operator: bool = False) -> bool:
        expected, values = equation
        current_values = {values[0]}
        for value in values[1:]:
            new_current_values = set()
            for current in current_values:
                new_add = current + value
                if new_add <= expected:
                    new_current_values.add(new_add)
                new_mul = current * value
                if new_mul <= expected:
                    new_current_values.add(new_mul)
                if additional_operator:
                    new_op = int(str(current) + str(value))
                    if new_op <= expected:
                        new_current_values.add(new_op)
            current_values = new_current_values
        return expected in current_values

    def solve1(self) -> int:
        result = 0
        for equation in self.equations:
            if self._is_valid(equation):
                result += equation[0]
        return result

    def solve2(self) -> int:
        result = 0
        for equation in self.equations:
            if self._is_valid(equation) or self._is_valid(equation, additional_operator=True):
                result += equation[0]
        return result


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
