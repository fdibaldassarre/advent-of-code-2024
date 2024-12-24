#!/usr/bin/env python
from typing import Dict, Tuple, Set, List


class LoopException(Exception):
    pass


class Gate:
    def __init__(self, inputs: Tuple[str, str], operation: str) -> None:
        self.inputs = inputs
        self.operation = operation

    def __call__(self, values: Dict[str, int]) -> int | None:
        v1 = values.get(self.inputs[0], None)
        v2 = values.get(self.inputs[1], None)
        if v1 is None or v2 is None:
            return None
        if self.operation == "AND":
            return v1 & v2
        elif self.operation == "OR":
            return v1 | v2
        elif self.operation == "XOR":
            return v1 ^ v2
        else:
            raise Exception(f"Unknown operation {self.operation}")


class Evaluator:

    def __init__(self, gates: Dict[str, Gate]) -> None:
        self.gates = gates
        self.parent_to_children: Dict[str, Set[str]] = {}
        for target, gate in self.gates.items():
            for input_gate in gate.inputs:
                if input_gate not in self.parent_to_children:
                    self.parent_to_children[input_gate] = set()
                self.parent_to_children[input_gate].add(target)

    def __call__(self, initial_values: Dict[str, int]) -> Dict[str, int]:
        values: Dict[str, int] = {}
        to_evaluate: Set[str] = set()
        for key, value in initial_values.items():
            values[key] = value
            if key not in self.parent_to_children:
                continue
            for child in self.parent_to_children[key]:
                to_evaluate.add(child)

        while len(to_evaluate) > 0:
            current = to_evaluate.pop()
            gate = self.gates[current]
            res = gate(values)
            if res is not None:
                if current in values:
                    raise LoopException()
                values[current] = res
                for child in self.parent_to_children.get(current, []):
                    to_evaluate.add(child)
        return values


class Tester:

    def __init__(self, gates: Dict[str, Gate]) -> None:
        self.evaluator = Evaluator(gates.copy())

    def swap(self, target1: str, target2: str) -> None:
        gates = self.evaluator.gates
        gates[target1], gates[target2] = gates[target2], gates[target1]
        self.evaluator = Evaluator(gates)

    def detect_loop(self, input_x: str, input_y: str, prev_rem: str | None) -> bool:
        initial_values = {input_x: 1, input_y: 1}
        if prev_rem is not None:
            initial_values[prev_rem] = 1
        try:
            self.evaluator(initial_values)
            return False
        except LoopException:
            return True

    def get_children(self, input_x: str, input_y: str, prev_rem: str | None) -> Set[str]:
        initial_values = {input_x: 1, input_y: 1}
        if prev_rem is not None:
            initial_values[prev_rem] = 1
        values = self.evaluator(initial_values)
        children = set(values.keys())
        children.remove(input_x)
        children.remove(input_y)
        if prev_rem is not None:
            children.remove(prev_rem)
        return children

    def evaluate_result(self, input_x: str, input_y: str, output_z: str, prev_rem: str | None) -> bool:
        if self.detect_loop(input_x, input_y, prev_rem):
            return False
        possible_rem = 1 if prev_rem is None else 2
        for rem in range(possible_rem):
            for x in range(2):
                for y in range(2):
                    initial_values = {input_x: x, input_y: y}
                    if prev_rem is not None:
                        initial_values[prev_rem] = rem
                    values = self.evaluator(initial_values)
                    if output_z not in values:
                        return False
                    z = values[output_z]
                    expected = x ^ y ^ rem
                    if z != expected:
                        # raise Exception(f"Unexpected output for {output_z}")
                        # print(f"Unexpected output for {output_z}")
                        return False
        return True

    def _get_candidate_rem(self, input_x: str, input_y: str, prev_rem: str | None) -> Set[str]:
        initial_values = {input_x: 1, input_y: 1}
        if prev_rem is not None:
            initial_values[prev_rem] = 1
        values = self.evaluator(initial_values)
        candidates: Set[str] = set()
        for candidate_rem in values.keys():
            if candidate_rem.startswith("x") or candidate_rem.startswith("y") or candidate_rem.startswith("z"):
                continue
            candidates.add(candidate_rem)
        return candidates

    def evaluate_remainder(self, input_x: str, input_y: str, prev_rem: str | None) -> str:
        candidate_rems: Set[str] = self._get_candidate_rem(input_x, input_y, prev_rem)
        possible_rem = 1 if prev_rem is None else 2
        for rem in range(possible_rem):
            for x in range(2):
                for y in range(2):
                    initial_values = {input_x: x, input_y: y}
                    if prev_rem is not None:
                        initial_values[prev_rem] = rem
                    values = self.evaluator(initial_values)
                    expected = (x & y) | (x & rem) | (y & rem)

                    to_be_removed: Set[str] = set()
                    for candidate in candidate_rems:
                        if values[candidate] != expected:
                            to_be_removed.add(candidate)
                    for el in to_be_removed:
                        candidate_rems.remove(el)

                    if len(candidate_rems) == 0:
                        raise Exception(f"All good values have been removed at {input_x}")
        if len(candidate_rems) != 1:
            raise Exception(f"Too many remainders, got {len(candidate_rems)}")
        return candidate_rems.pop()

    def attempt_fix(
        self, input_x: str, input_y: str, prev_rem: str | None, output_z: str, gates_to_swap: Set[str]
    ) -> Tuple[str, str]:
        swap_candidates = self.get_children(input_x, input_y, prev_rem=prev_rem)
        fixes: Set[Tuple[str, str]] = set()
        for candidate in swap_candidates:
            for other in gates_to_swap:
                if candidate == other:
                    continue
                # Swap
                self.swap(candidate, other)
                # Test
                if self.evaluate_result(input_x, input_y, output_z, prev_rem=prev_rem):
                    normalized = [candidate, other]
                    normalized.sort()
                    fixes.add(tuple(normalized))
                self.swap(other, candidate)
        if len(fixes) != 1:
            print(fixes)
            raise Exception(f"Could not fix {output_z}")
        else:
            candidate, other = fixes.pop()
            print(f"Actual fix!!! {candidate} <> {other}")
            self.swap(candidate, other)
            return candidate, other


class Solver:

    def __init__(self):
        self.initial_values: Dict[str, int] = {}
        self.gates: Dict[str, Gate] = {}
        self.out_gates: List[str] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                if line == "":
                    break
                gid, val = line.split(": ", maxsplit=1)
                self.initial_values[gid] = int(val)
            for line in hand:
                line = line.strip()
                input_data, target = line.split(" -> ", maxsplit=1)
                input1, op, input2 = input_data.split(" ", maxsplit=2)
                self.gates[target] = Gate((input1, input2), operation=op)

            for gid in self.gates.keys():
                if gid.startswith("z"):
                    self.out_gates.append(gid)
            self.out_gates.sort()

    def solve1(self) -> int:
        evaluator = Evaluator(self.gates)
        values = evaluator(self.initial_values)
        res = 0
        for n, gid in enumerate(self.out_gates):
            res += values[gid] * (2**n)
        return res

    def solve2(self) -> str:
        gates_to_swap: Set[str] = {gid for gid in self.gates.keys()}
        tester = Tester(self.gates)
        prev_rem: str | None = None
        fixes: List[str] = []
        for i, output_z in enumerate(self.out_gates):
            input_x = "x%02d" % i
            input_y = "y%02d" % i

            if not tester.evaluate_result(input_x, input_y, output_z, prev_rem=prev_rem):
                sw1, sw2 = tester.attempt_fix(
                    input_x, input_y, prev_rem=prev_rem, output_z=output_z, gates_to_swap=gates_to_swap
                )
                fixes.append(sw1)
                fixes.append(sw2)

            used_gates = tester.get_children(input_x, input_y, prev_rem=prev_rem)
            for gid in used_gates:
                gates_to_swap.remove(gid)
            prev_rem = tester.evaluate_remainder(input_x, input_y, prev_rem=prev_rem)

            if i == 43:
                break

        fixes.sort()
        return ",".join(fixes)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %s" % solution2)


if __name__ == "__main__":
    main()
