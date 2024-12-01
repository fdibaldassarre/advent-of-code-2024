#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.left_list = []
        self.right_list = []

    def parse(self, path: str) -> None:
        with open(path, "r") as hand:
            for line in hand:
                line = line.strip()
                n1, n2 = tuple(map(int, line.split()))
                self.left_list.append(n1)
                self.right_list.append(n2)

    def solve1(self) -> int:
        self.left_list.sort()
        self.right_list.sort()
        total = 0
        for n1, n2 in zip(self.left_list, self.right_list):
            total += abs(n1 - n2)
        return total

    def solve2(self) -> int:
        occurrences = {}
        for value in self.right_list:
            occurrences[value] = occurrences.get(value, 0) + 1
        score = 0
        for n in self.left_list:
            score += n * occurrences.get(n, 0)
        return score


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
