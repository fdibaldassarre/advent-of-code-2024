#!/usr/bin/env python
from typing import Tuple, Generator, List, Set

Point = Tuple[int, int]
Direction = Tuple[int, int]
RegionInfo = Tuple[int, int, int]


def vector_diff(point1: Point, point2: Point) -> Direction:
    return point1[0] - point2[0], point1[1] - point2[1]


class Side:
    """def __init__(self, point1: Point, point2: Point):
    points = [point1, point2]
    points.sort()
    self.points = tuple(points)"""

    def __init__(self, is_vertical: bool, height: int, start: Point, direction: Direction) -> None:
        self.is_vertical = is_vertical
        self.height = height
        self.start = start
        self.direction = direction

    @staticmethod
    def new(point1: Point, point2: Point) -> "Side":
        points = [point1, point2]
        direction = vector_diff(point2, point1)
        points.sort()
        p1, p2 = points
        is_vertical = p1[0] == p2[0]
        if is_vertical:
            return Side(True, p1[0], (p1[1], p2[1]), direction)
        else:
            assert p1[1] == p2[1]
            return Side(False, p1[1], (p1[0], p2[0]), direction)

    def __hash__(self):
        return hash((self.is_vertical, self.height, self.start, self.direction))

    def __eq__(self, other: "Side"):
        return (
            self.is_vertical
            and other.is_vertical
            and self.height == other.height
            and self.start == other.start
            and self.direction == other.direction
        )

    def __repr__(self):
        return f"Side {self.is_vertical}, {self.height}, {self.start}"

    def to_tuple(self):
        return self.is_vertical, self.start, self.height, self.direction

    def is_right_after(self, prev_side: "Side") -> bool:
        if self.is_vertical != prev_side.is_vertical:
            return False
        if self.start != prev_side.start:
            return False
        if self.direction != prev_side.direction:
            return False
        return prev_side.height + 1 == self.height


class Solver:

    def __init__(self):
        self.data = list()
        self.width = 0
        self.height = 0

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)
        self.width = len(self.data[0])
        self.height = len(self.data)

    def _get_ch_at(self, point: Point) -> str | None:
        y, x = point
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.data[y][x]
        else:
            return None

    def _get_neighbours(self, point: Point) -> Generator[Point, None, None]:
        y, x = point
        yield y + 1, x
        yield y - 1, x
        yield y, x + 1
        yield y, x - 1

    def _count_sides(self, sides_set: Set[Side]) -> int:
        n_sides = 1
        sides = list(sides_set)
        sides.sort(key=lambda el: el.to_tuple())
        for i in range(1, len(sides)):
            prev_side = sides[i - 1]
            next_side = sides[i]
            if not next_side.is_right_after(prev_side):
                n_sides += 1
        return n_sides

    def _explore(self) -> Generator[RegionInfo, None, None]:
        boundary = {(0, 0)}
        explored = set()
        while len(boundary) > 0:
            point = boundary.pop()
            if point in explored:
                continue
            ch = self._get_ch_at(point)
            area_points = {point}
            region_area = 0
            region_perimeter = 0
            region_sides = set()
            while len(area_points) > 0:
                new_point = area_points.pop()
                if new_point in explored:
                    continue
                for neighbour in self._get_neighbours(new_point):
                    n_ch = self._get_ch_at(neighbour)
                    if n_ch == ch:
                        area_points.add(neighbour)
                    else:
                        region_perimeter += 1
                        region_sides.add(Side.new(new_point, neighbour))
                        if n_ch is not None:
                            boundary.add(neighbour)
                region_area += 1
                explored.add(new_point)
            sides = self._count_sides(region_sides)
            yield region_area, region_perimeter, sides

    def solve1(self) -> int:
        total_price = 0
        for region_area, region_perimeter, _ in self._explore():
            total_price += region_area * region_perimeter
        return total_price

    def solve2(self) -> int:
        total_price = 0
        for region_area, _, num_sides in self._explore():
            total_price += region_area * num_sides
        return total_price


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
