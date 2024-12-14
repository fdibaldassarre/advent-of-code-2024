#!/usr/bin/env python
import collections
from typing import Tuple, List, Dict, Set

Point = Tuple[int, int]
Vector = Tuple[int, int]


class MapSpace:

    def __init__(self, characteristic: Tuple[int, int]) -> None:
        self.characteristic = characteristic
        self.mid_x, self.mid_y = self.characteristic[0] // 2, self.characteristic[1] // 2

    def vector_sum(self, point: Point, direction: Vector) -> Point:
        return tuple((x + d) % ch for x, d, ch in zip(point, direction, self.characteristic))

    def scalar_prod(self, k: int, vector: Vector) -> Point:
        return tuple((k * v) % ch for v, ch in zip(vector, self.characteristic))

    def get_quadrant(self, point: Tuple[int, int]) -> Tuple[int, int] | None:
        x, y = point
        if x == self.mid_x or y == self.mid_y:
            return None
        qx = min(1, x // self.mid_x)
        qy = min(1, y // self.mid_y)
        return qx, qy


def print_map(size: Tuple[int, int], points: Set[Point]) -> None:
    w, h = size
    for y in range(h):
        line = [" " for _ in range(w)]
        for x in range(w):
            if (x, y) in points:
                line[x] = "#"  # str(points[(x, y)])
        print("".join(line))


def _print_quadrants(size, quadrant_map):
    w, h = size
    for y in range(h):
        line = ["" for _ in range(w)]
        for x in range(w):
            line[x] = quadrant_map[(x, y)]
        print("".join(line))


QT_MAP = {
    (0, 0): "A",
    (1, 0): "B",
    (0, 1): "C",
    (1, 1): "D",
}


class Solver:

    def __init__(self):
        self.robot_positions: List[Tuple[Point, Vector]] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for el in hand:
                p_raw, v_raw = el.split(" ")
                pos = tuple(int(el) for el in p_raw[2:].split(","))
                speed = tuple(int(el) for el in v_raw[2:].split(","))
                self.robot_positions.append((pos, speed))

    def solve1(self) -> int:
        map_space = MapSpace((101, 103))
        quadrants = collections.defaultdict(int)
        for position in self.robot_positions:
            start, direction = position
            new_pos = map_space.vector_sum(start, map_space.scalar_prod(100, direction))
            quadrant = map_space.get_quadrant(new_pos)
            if quadrant is not None:
                quadrants[quadrant] += 1

        res = 1
        for el in quadrants.values():
            res *= el
        return res

    def solve2(self) -> int:
        size = (101, 103)
        map_space = MapSpace(size)
        k = 0
        while True:
            k += 1
            positions = set()
            all_unique = True
            for robot in self.robot_positions:
                start, direction = robot
                new_pos = map_space.vector_sum(start, map_space.scalar_prod(k, direction))
                if new_pos in positions:
                    all_unique = False
                    break
                positions.add(new_pos)
            if all_unique:
                print_map(size, positions)
                break

        return k


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
