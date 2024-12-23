#!/usr/bin/env python
from typing import Tuple, List, Dict, Set


class Solver:

    def __init__(self):
        self._graph: List[Tuple[str, str]] = []
        self._connections: Dict[str, Set[str]] = {}

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self._graph.append(tuple(line.split("-", maxsplit=1)))
        for pair in self._graph:
            a, b = pair
            if a not in self._connections:
                self._connections[a] = set()
            if b not in self._connections:
                self._connections[b] = set()
            self._connections[a].add(b)
            self._connections[b].add(a)

    def solve1(self) -> int:
        valid_pairs: Set[Tuple[str, str, str]] = set()
        for key, connected in self._connections.items():
            if len(connected) < 2:
                continue
            if not key.startswith("t"):
                continue
            connected_list = list(connected)
            for i in range(len(connected_list) - 1):
                a = connected_list[i]
                for j in range(i + 1, len(connected_list)):
                    b = connected_list[j]
                    if a in self._connections[b]:
                        candidate = [key, a, b]
                        candidate.sort()
                        valid_pairs.add(tuple(candidate))
        return len(valid_pairs)

    def _expand_cluster(self, points: List[str], current_cluster: Set[str]) -> Set[str]:
        if len(points) == 0:
            return current_cluster
        if len(current_cluster) == 0:
            return current_cluster
        if points[0] not in current_cluster:
            return self._expand_cluster(points[1:], current_cluster)

        keep = current_cluster.intersection(self._connections[points[0]])
        keep.add(points[0])
        option_1 = self._expand_cluster(points[1:], keep)
        current_cluster.remove(points[0])
        option_2 = self._expand_cluster(points[1:], current_cluster)
        if len(option_1) > len(option_2):
            return option_1
        else:
            return option_2

    def solve2(self) -> str:
        max_cluster: Set[str] = set()
        for key, connections in self._connections.items():
            base_cluster = connections.copy()
            base_cluster.add(key)
            candidate: Set[str] = self._expand_cluster(list(connections), base_cluster)
            if len(candidate) > len(max_cluster):
                max_cluster = candidate
        candidate_sorted = list(max_cluster)
        candidate_sorted.sort()
        return ",".join(candidate_sorted)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %s" % solution2)


if __name__ == "__main__":
    main()
