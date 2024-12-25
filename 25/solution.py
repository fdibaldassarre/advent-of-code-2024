#!/usr/bin/env python
from typing import Tuple, List

Schematic = Tuple[int, int, int, int, int]


class Solver:

    def __init__(self):
        self.keys: List[Schematic] = list()
        self.locks: List[Schematic] = list()

    def _parse_schematic(self, schema: List[str]) -> Schematic:
        schematic: List[int] = [0, 0, 0, 0, 0]
        for i in range(5):
            for line in schema:
                if line[i] == "#":
                    schematic[i] += 1
        return tuple(schematic)

    def parse(self, path: str) -> None:
        with open(path) as hand:
            schema: List[str] = []
            for line in hand:
                line = line.strip()
                if line == "":
                    continue
                schema.append(line)
                if len(schema) == 7:
                    is_lock = schema[0].startswith(".")
                    schema = schema[1:-1]
                    if is_lock:
                        self.keys.append(self._parse_schematic(schema))
                    else:
                        self.locks.append(self._parse_schematic(schema))
                    schema = []

    def solve1(self) -> int:
        fit_pairs = 0
        for key in self.keys:
            for lock in self.locks:
                if all(key[i] + lock[i] <= 5 for i in range(5)):
                    fit_pairs += 1
        return fit_pairs


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)


if __name__ == "__main__":
    main()
