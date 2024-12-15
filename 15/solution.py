#!/usr/bin/env python
import collections
from typing import Tuple, Dict, Iterable, List, Set, Deque

CH_ROBOT = "@"
CH_WALL = "#"
CH_BOX = "O"
CH_SPACE = "."
CH_BOX_LEFT = "["
CH_BOX_RIGHT = "]"

MOVEMENTS = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}

Point = Tuple[int, int]
Box = Tuple[Point, Point]


def vector_sum(point: Point, direction: Tuple[int, int]) -> Point:
    return point[0] + direction[0], point[1] + direction[1]


class Solver:

    def __init__(self):
        self.warehouse = dict()
        self.warehouse_width = 0
        self.warehouse_height = 0
        self.robot = None
        self.moves = list()

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                if line.startswith("#"):
                    self.warehouse_width = len(line)
                    self.warehouse_height = y + 1
                if line == "":
                    break
                for x, ch in enumerate(line):
                    if ch == CH_ROBOT:
                        self.robot = (x, y)
                        self.warehouse[(x, y)] = CH_SPACE
                    else:
                        self.warehouse[(x, y)] = ch
            for line in hand:
                line = line.strip()
                for ch in line:
                    self.moves.append(ch)

    def _print_warehouse(self, positions: Dict[Point, str], robot: Point, expanded: bool = False) -> None:
        width = self.warehouse_width
        height = self.warehouse_height
        if expanded:
            width = width * 2
        for y in range(height):
            line = [positions[(x, y)] for x in range(width)]
            if y == robot[1]:
                line[robot[0]] = "@"
            line = "".join(line)
            print(line)

    def _push(self, robot: Point, move: str, positions: Dict[Point, str]) -> Point:
        direction = MOVEMENTS[move]
        next_robot = vector_sum(robot, direction)
        box_end = next_robot
        has_free = False
        while 0 <= box_end[0] < self.warehouse_width and 0 <= box_end[1] < self.warehouse_height:
            if positions[box_end] == CH_WALL:
                break
            if positions[box_end] == CH_SPACE:
                has_free = True
                break
            box_end = vector_sum(box_end, direction)
        if not has_free:
            return robot
        else:
            # Move
            positions[box_end] = positions[next_robot]
            positions[next_robot] = CH_SPACE
            return next_robot

    def solve1(self) -> int:
        positions = self.warehouse.copy()
        robot = self.robot
        for move in self.moves:
            robot = self._push(robot, move, positions)
        total_gps = 0
        for pos, ch in positions.items():
            if ch == CH_BOX:
                x, y = pos
                total_gps += x + 100 * y
        return total_gps

    def _expanded_map(self) -> Dict[Point, str]:
        expanded: Dict[Point, str] = dict()
        for pos, ch in self.warehouse.items():
            x, y = pos
            if ch == CH_BOX:
                expanded[(2 * x, y)] = CH_BOX_LEFT
                expanded[(2 * x + 1, y)] = CH_BOX_RIGHT
            else:
                expanded[(2 * x, y)] = ch
                expanded[(2 * x + 1, y)] = ch
        return expanded

    def _push_horizontal(self, robot: Point, direction: Tuple[int, int], positions: Dict[Point, str]) -> Point:
        next_robot = vector_sum(robot, direction)
        box_end = next_robot
        has_free = False
        boxes = collections.deque()
        while 0 <= box_end[0] < 2 * self.warehouse_width:
            if positions[box_end] == CH_WALL:
                break
            if positions[box_end] == CH_SPACE:
                has_free = True
                break
            boxes.append(box_end)
            box_end = vector_sum(box_end, direction)
        if not has_free:
            return robot
        else:
            # Move
            if len(boxes) == 0:
                return next_robot
            positions[box_end] = positions[next_robot]
            positions[next_robot] = CH_SPACE
            boxes.popleft()
            boxes.append(box_end)
            for box in boxes:
                if positions[box] == CH_BOX_LEFT:
                    positions[box] = CH_BOX_RIGHT
                elif positions[box] == CH_BOX_RIGHT:
                    positions[box] = CH_BOX_LEFT
                else:
                    raise Exception("Unexpected")
            return next_robot

    def _get_pushable_box(self, box: Box, direction: Tuple[int, int], positions: Dict[Point, str]) -> List[Box] | None:
        can_be_pushed = True
        pushable_boxes: List[Box] = []
        for point in box:
            next_point = vector_sum(point, direction)
            if positions[next_point] == CH_WALL:
                can_be_pushed = False
                break
            elif positions[next_point] == CH_BOX_LEFT:
                pushable_boxes.append((next_point, vector_sum(next_point, (1, 0))))
            elif positions[next_point] == CH_BOX_RIGHT:
                pushable_boxes.append((vector_sum(next_point, (-1, 0)), next_point))
        if can_be_pushed:
            return pushable_boxes
        else:
            return None

    def _get_pushable(
        self, box: Box, direction: Tuple[int, int], positions: Dict[Point, str]
    ) -> Iterable[Set[Box]] | None:
        is_pushable = True
        border = {box}
        pushable_queue: Deque[Set[Box]] = collections.deque()
        while is_pushable and len(border) > 0:
            pushable_queue.append(border)
            new_border = set()
            for box in border:
                push_up = self._get_pushable_box(box, direction, positions)
                if push_up is None:
                    is_pushable = False
                    break
                new_border.update(push_up)
            border = new_border

        if is_pushable:
            pushable_queue.reverse()
            return pushable_queue
        else:
            return None

    def _push_boxes(
        self, all_boxes: Iterable[Set[Box]], direction: Tuple[int, int], positions: Dict[Point, str]
    ) -> None:
        for level in all_boxes:
            for box in level:
                for point in box:
                    if positions[vector_sum(point, direction)] != CH_SPACE:
                        raise Exception("Unexpected non space")
                    positions[vector_sum(point, direction)] = positions[point]
                    positions[point] = CH_SPACE

    def _push_vertical(self, robot: Point, direction: Tuple[int, int], positions: Dict[Point, str]) -> Point:
        next_robot = vector_sum(robot, direction)
        if positions[next_robot] == CH_SPACE:
            return next_robot
        elif positions[next_robot] == CH_WALL:
            return robot
        if positions[next_robot] == CH_BOX_RIGHT:
            box = vector_sum(next_robot, (-1, 0)), next_robot
        else:
            box = next_robot, vector_sum(next_robot, (1, 0))
        pushable = self._get_pushable(box, direction, positions)
        if pushable is None:
            return robot
        else:
            self._push_boxes(pushable, direction, positions)
            return next_robot

    def _push_expanded(self, robot: Point, move: str, positions: Dict[Point, str]) -> Point:
        direction = MOVEMENTS[move]
        if direction[1] == 0:
            return self._push_horizontal(robot, direction, positions)
        else:
            return self._push_vertical(robot, direction, positions)

    def solve2(self) -> int:
        positions = self._expanded_map()
        robot = self.robot[0] * 2, self.robot[1]
        for move in self.moves:
            robot = self._push_expanded(robot, move, positions)

        total_gps = 0
        for pos, ch in positions.items():
            if ch == CH_BOX_LEFT:
                x, y = pos
                total_gps += x + 100 * y
        return total_gps


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
