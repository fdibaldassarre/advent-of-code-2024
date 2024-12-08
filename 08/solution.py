#!/usr/bin/env python
import math
from typing import Tuple, Dict, Set, List

Point = Tuple[int, int]
Vector = Tuple[int, int]


def vector_diff(p1: Point, p2: Point) -> Vector:
    return p1[0] - p2[0], p1[1] - p2[1]


def vector_sum(p: Point, v: Vector) -> Point:
    return p[0] + v[0], p[1] + v[1]


def vector_prod(n: int, v: Vector) -> Vector:
    return n * v[0], n * v[1]


def reduce(v: Vector) -> Vector:
    y, x = v
    if y == 0:
        return 0, 1
    if x == 0:
        return 1, 0
    d = math.gcd(x, y)
    return y // d, x // d


class Solver:

    def __init__(self):
        self.city = []
        self.width = 0
        self.height = 0
        self.antennas: Dict[str, List[Point]] = dict()

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                self.city.append(line)
                for x, ch in enumerate(line):
                    if ch != ".":
                        if ch not in self.antennas:
                            self.antennas[ch] = list()
                        self.antennas[ch].append((y, x))
        self.height = len(self.city)
        self.width = len(self.city[0])

    def _is_inside_map(self, point: Point) -> bool:
        return 0 <= point[0] < self.height and 0 <= point[1] < self.width

    def solve1(self) -> int:
        antinodes = set()
        for positions in self.antennas.values():
            for position in positions:
                for other in positions:
                    if position == other:
                        continue
                    delta = vector_diff(position, other)
                    antinode = vector_sum(position, delta)
                    if self._is_inside_map(antinode):
                        antinodes.add(antinode)
        return len(antinodes)

    def _get_nodes_on(self, point: Point, direction: Vector) -> Set[Point]:
        nodes = set()
        for sgn in [-1, 1]:
            node = point
            d = 0
            while self._is_inside_map(node):
                nodes.add(node)
                d += sgn
                node = vector_sum(point, vector_prod(d, direction))
        return nodes

    def __print_antinodes(self, nodes):
        city_map = list()
        for _ in range(self.height):
            city_map.append(["."] * self.width)
        for node in nodes:
            y, x = node
            city_map[y][x] = "#"
        printable = ["".join(line) for line in city_map]
        print("\n".join(printable))

    def solve2(self) -> int:
        antinodes: Set[Point] = set()
        for positions in self.antennas.values():
            for i, position in enumerate(positions):
                for j in range(i + 1, len(positions)):
                    other = positions[j]
                    delta = vector_diff(position, other)
                    delta_min = reduce(delta)
                    nodes = self._get_nodes_on(position, delta_min)
                    antinodes.update(nodes)
        return len(antinodes)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
