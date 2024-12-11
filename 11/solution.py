#!/usr/bin/env python

import collections
import functools
from typing import Tuple


class Solver:

    def __init__(self):
        self.stones = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            line = hand.read().split(" ")
            self.stones = [int(n) for n in line]

    def _get_next_stones(self, stone: int) -> Tuple[int, ...]:
        if stone == 0:
            return (1,)
        elif len(str(stone)) % 2 == 0:
            stone_str = str(stone)
            return int(stone_str[: len(stone_str) // 2]), int(stone_str[len(stone_str) // 2 :])
        else:
            return (stone * 2024,)

    def solve1(self) -> int:
        stones = collections.deque(self.stones)
        for _ in range(25):
            new_stones = collections.deque()
            for stone in stones:
                for new_stone in self._get_next_stones(stone):
                    new_stones.append(new_stone)
            stones = new_stones
        return len(stones)

    def solve2(self) -> int:
        stones = collections.defaultdict(int)
        for stone in self.stones:
            stones[stone] += 1
        for _ in range(75):
            new_stones = collections.defaultdict(int)
            for stone, n_stones in stones.items():
                for new_stone in self._get_next_stones(stone):
                    new_stones[new_stone] += n_stones
            stones = new_stones
        return sum(stones.values())


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
