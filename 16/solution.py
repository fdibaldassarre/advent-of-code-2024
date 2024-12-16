#!/usr/bin/env python
import collections
import heapq
from typing import Tuple, Any, Generator, Set, List, Dict, Deque

Point = Tuple[int, int]
Direction = Tuple[int, int]


def vector_sum(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def vector_diff(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def sgn(a: int) -> int:
    if a == 0:
        return 0
    else:
        return 1 if a > 0 else -1


def vector_sgn(a: Tuple[int, int]) -> Tuple[int, int]:
    return sgn(a[0]), sgn(a[1])


def scalar_prod(k: int, v: Tuple[int, int]) -> Tuple[int, int]:
    return k * v[0], k * v[1]


def turn_right(direction: Direction) -> Direction:
    return direction[1], -1 * direction[0]


def turn_left(direction: Direction) -> Direction:
    return -1 * direction[1], direction[0]


COST_MOVE = 1
COST_TURN = 1000

MazePositionIde = Tuple[Point, Direction, int]


class MazePosition:

    def __init__(self, position: Point, direction: Direction, score: int) -> None:
        self.position = position
        self.direction = direction
        self.score = score

    def to_map_position(self) -> Tuple[Point, Direction]:
        return self.position, self.direction

    def to_tuple(self, estimated_score: int) -> Tuple[int, Any]:
        return estimated_score, (self.score, self.position, self.direction)

    def to_ide(self) -> MazePositionIde:
        return self.position, self.direction, self.score

    @classmethod
    def from_tuple(cls, value: Tuple[int, Any]) -> "MazePosition":
        _, values = value
        score, position, direction = values
        return cls(position=position, direction=direction, score=score)


class Solver:

    def __init__(self):
        self.maze = None
        self.start_point = None
        self.end_point = None

    def parse(self, path: str) -> None:
        self.maze = list()
        with open(path) as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                row = [ch for ch in line]
                for x, ch in enumerate(row):
                    if ch == "S":
                        self.start_point = (x, y)
                        row[x] = "."
                    elif ch == "E":
                        self.end_point = (x, y)
                        row[y] = "."
                self.maze.append(row)

    def estimate_needed_score(self, position: Point, direction: Tuple[int, int]) -> int:
        direction_to_end = vector_sgn(vector_diff(self.end_point, position))
        n_turns = 0
        if direction_to_end != direction:
            n_turns = 1
            for i in range(2):
                if direction[i] != 0 and direction[i] == -1 * direction_to_end[i]:
                    n_turns = 2
        delta = vector_diff(self.end_point, position)
        distance = abs(delta[0]) + (delta[1])
        return n_turns * COST_TURN + distance * COST_MOVE

    def get_next_positions(self, maze_position: MazePosition) -> Generator[MazePosition, None, None]:
        # Front
        x, y = vector_sum(maze_position.position, maze_position.direction)
        if self.maze[y][x] != "#":
            new_score = maze_position.score + COST_MOVE
            yield MazePosition((x, y), direction=maze_position.direction, score=new_score)
        # Left
        score_turn = maze_position.score + COST_TURN
        direction_left = turn_left(maze_position.direction)
        yield MazePosition(maze_position.position, direction=direction_left, score=score_turn)
        direction_right = turn_right(maze_position.direction)
        yield MazePosition(maze_position.position, direction=direction_right, score=score_turn)

    def _convert_to_tuple(self, maze_position: MazePosition) -> Tuple[int, Any]:
        estimate_cost = self.estimate_needed_score(maze_position.position, maze_position.direction)
        estimate_score = maze_position.score + estimate_cost
        return maze_position.to_tuple(estimate_score)

    def solve(self) -> Tuple[List[MazePosition], Dict[MazePositionIde, Set[MazePositionIde]]]:
        start_position = MazePosition(self.start_point, (1, 0), score=0)
        border = []
        heapq.heapify(border)
        heapq.heappush(border, self._convert_to_tuple(start_position))
        best_score = None
        top_paths: List[MazePosition] = list()
        explored: Set[Tuple[Point, Direction]] = set()
        parents: Dict[MazePositionIde, Set[MazePositionIde]] = {start_position.to_ide(): set()}
        while best_score is None:
            current = heapq.heappop(border)
            pos = MazePosition.from_tuple(current)
            pos_ide = pos.to_ide()
            map_pos = pos.to_map_position()
            if map_pos in explored:
                continue
            explored.add(map_pos)
            if best_score is not None and pos.score > best_score:
                break
            if pos.position == self.end_point:
                best_score = pos.score
                top_paths.append(pos)
                continue
            for new_pos in self.get_next_positions(pos):
                heapq.heappush(border, self._convert_to_tuple(new_pos))
                new_pos_ide = new_pos.to_ide()
                if new_pos_ide not in parents:
                    parents[new_pos_ide] = set()
                parents[new_pos.to_ide()].add(pos_ide)
        return top_paths, parents

    def solve1(self) -> int:
        best_maze_positions, _ = self.solve()
        return best_maze_positions[0].score

    def solve2(self) -> int:
        best_maze_positions, parents = self.solve()
        explore: Deque[MazePositionIde] = collections.deque()
        explore.extend([pos.to_ide() for pos in best_maze_positions])
        visited: Set[Point] = set()
        while len(explore) > 0:
            pos_ide = explore.pop()
            for el in parents[pos_ide]:
                explore.append(el)
            point, _, _ = pos_ide
            visited.add(point)

        return len(visited)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
