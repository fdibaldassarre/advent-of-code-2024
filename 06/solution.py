#!/usr/bin/env python
from typing import Tuple, Set

GUARD = {"^": (-1, 0), ">": (0, 1), "V": (1, 0), "<": (0, -1)}
DIRECTION_TO_GUARD = {value: key for key, value in GUARD.items()}

Point = Tuple[int, int]
Direction = Tuple[int, int]


def vector_sum(point: Point, direction: Direction) -> Point:
    result = []
    for p, d in zip(point, direction):
        result.append(p + d)
    return tuple(result)


def turn_right(direction: Direction) -> Direction:
    y, x = direction
    return x, -y


class Solver:

    def __init__(self):
        self.floor = None
        self.start_position = None
        self.start_direction = None
        self.height = -1
        self.width = -1

    def parse(self, path: str) -> None:
        self.floor = []
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                for x, ch in enumerate(line):
                    if ch in GUARD:
                        self.start_position = (len(self.floor), x)
                        self.start_direction = GUARD[ch]
                        line = line.replace(ch, ".")
                        break
                self.floor.append(line)
        self.height = len(self.floor)
        self.width = len(self.floor[0])

    def _is_outside(self, point: Point) -> bool:
        y, x = point
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def _is_obstacle(self, point: Point) -> bool:
        y, x = point
        ch = self.floor[y][x]
        return ch == "#"

    def _print(self, current: Point, direction: Direction) -> None:
        status = []
        for y, line in enumerate(self.floor):
            status.append([ch for ch in line])
        cy, cx = current
        status[cy][cx] = DIRECTION_TO_GUARD[direction]
        res = ["".join(line) for line in status]
        print("\n".join(res))

    def _move(
        self, current: Point, direction: Direction, extra_obstacle: Point | None = None
    ) -> Tuple[Point, Direction] | None:
        next_step = vector_sum(current, direction)
        if self._is_outside(next_step):
            return None
        elif self._is_obstacle(next_step) or next_step == extra_obstacle:
            direction = turn_right(direction)
            return current, direction
        else:
            # Move
            return next_step, direction

    def _get_visited(self) -> Set[Point]:
        visited = set()
        point, direction = self.start_position, self.start_direction
        while True:
            visited.add(point)
            next_position = self._move(point, direction)
            if next_position is None:
                break
            point, direction = next_position
        return visited

    def solve1(self) -> int:
        visited = self._get_visited()
        return len(visited)

    def _is_loop_with_obstacle(
        self, point: Point, direction: Direction, obstacle: Point, visited: Set[Tuple[Point, Direction]]
    ) -> bool:
        is_loop = False
        while True:
            visited.add((point, direction))
            next_position = self._move(point, direction, extra_obstacle=obstacle)
            if next_position is None:
                break
            elif next_position in visited:
                is_loop = True
                break
            point, direction = next_position
        return is_loop

    def solve2(self) -> int:
        visited: Set[Tuple[Point, Direction]] = set()
        point, direction = self.start_position, self.start_direction
        checked: Set[Point] = set()
        checked.add(self.start_position)
        obstacles_that_cause_loop = 0
        while True:
            visited.add((point, direction))
            next_position = self._move(point, direction)
            if next_position is None:
                break
            obstacle = next_position[0]
            if obstacle not in checked and self._is_loop_with_obstacle(point, direction, obstacle, visited.copy()):
                obstacles_that_cause_loop += 1
            checked.add(obstacle)
            point, direction = next_position
        return obstacles_that_cause_loop


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
