#!/usr/bin/env python
import collections
import functools
from typing import List, Tuple, Dict, Set

ChangeSequence = Tuple[int, int, int, int]


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


class Solver:

    def __init__(self):
        self.secrets: List[int] = list()

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.secrets.append(int(line))

    def _get_next_secret_number(self, secret: int) -> int:
        secret = prune(mix(secret * 64, secret))
        secret = prune(mix(secret // 32, secret))
        return prune(mix(secret * 2048, secret))

    def solve1(self) -> int:
        total = 0
        for secret in self.secrets:
            for _ in range(2000):
                secret = self._get_next_secret_number(secret)
            total += secret
        return total

    def _get_prices(self, secret: int) -> List[int]:
        prices: List[int] = [secret % 10]
        for _ in range(2000):
            secret = self._get_next_secret_number(secret)
            prices.append(secret % 10)
        return prices

    def _get_sequence_to_price(self, secret: int) -> Dict[ChangeSequence, int]:
        prices = self._get_prices(secret)
        sequence = collections.deque()
        sequence_to_price: Dict[ChangeSequence, int] = collections.defaultdict(int)
        for i in range(1, len(prices)):
            delta = prices[i] - prices[i - 1]
            sequence.append(delta)
            if len(sequence) > 4:
                sequence.popleft()
            if len(sequence) == 4:
                change_seq = tuple(sequence)
                if change_seq not in sequence_to_price:
                    sequence_to_price[change_seq] = prices[i]
        return sequence_to_price

    def solve2(self) -> int:
        sequence_to_value: Dict[ChangeSequence, int] = collections.defaultdict(int)
        max_sell = 0
        for secret in self.secrets:
            sequence_to_sell = self._get_sequence_to_price(secret)
            for sequence, price in sequence_to_sell.items():
                sequence_to_value[sequence] += price
                if sequence_to_value[sequence] > max_sell:
                    max_sell = sequence_to_value[sequence]
        return max_sell


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
