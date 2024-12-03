#!/usr/bin/env python
from typing import Tuple


class Solver:

    def __init__(self):
        self.memory = None

    def parse(self, path: str) -> None:
        with open(path) as hand:
            self.memory = hand.read().strip()

    def _get_number_at(self, idx: int) -> Tuple[int,int] | None:
        start = idx
        while idx < len(self.memory):
            if ord("0") <= ord(self.memory[idx]) <= ord("9"):
                idx += 1
            else:
                break
        if start == idx:
            return None
        else:
            return int(self.memory[start:idx]), idx
    def _scan_multiplication_at(self, idx: int) -> Tuple[int,int] | None:
        if idx + 6 >= len(self.memory):
            return None
        if self.memory[idx:idx+4] != "mul(":
            return None
        first_num_and_next_idx = self._get_number_at(idx + 4)
        if first_num_and_next_idx is None:
            return None
        first_num, next_idx = first_num_and_next_idx
        if next_idx >= len(self.memory) or self.memory[next_idx] != ",":
            return None
        second_num_and_last_idx = self._get_number_at(next_idx + 1)
        if next_idx >= len(self.memory) or second_num_and_last_idx is None:
            return None
        second_num, last_idx = second_num_and_last_idx
        if next_idx >= len(self.memory) or self.memory[last_idx] != ")":
            return None
        return first_num * second_num, last_idx + 1

    def solve1(self) -> int:
        idx = 0
        result = 0
        while idx < len(self.memory):
            if self.memory[idx] != "m":
                idx += 1
                continue
            value_and_next_idx = self._scan_multiplication_at(idx)
            if value_and_next_idx is None:
                idx += 1
                continue
            value, idx = value_and_next_idx
            result += value
        return result

    def _scan_do_dont(self, idx) -> Tuple[bool, int] | None:
        if self.memory[idx:idx+4] == "do()":
            return True, idx + 4
        elif self.memory[idx:idx+7] == "don't()":
            return False, idx+7
        else:
            return None

    def solve2(self) -> int:
        idx = 0
        result = 0
        multiplication_enabled = True
        while idx < len(self.memory):
            if self.memory[idx] == "d":
                do_and_next_idx = self._scan_do_dont(idx)
                if do_and_next_idx is None:
                    idx += 1
                    continue
                do, idx = do_and_next_idx
                if do:
                    multiplication_enabled = True
                else:
                    multiplication_enabled = False
            if self.memory[idx] == "m" and multiplication_enabled:
                value_and_next_idx = self._scan_multiplication_at(idx)
                if value_and_next_idx is None:
                    idx += 1
                    continue
                value, idx = value_and_next_idx
                result += value
            else:
                idx += 1
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
