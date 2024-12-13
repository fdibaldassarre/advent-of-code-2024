#!/usr/bin/env python
import dataclasses
import math
from typing import Tuple, List, Generator, Set

Vector = Tuple[int, int]


@dataclasses.dataclass
class Machine:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    prize: Tuple[int, int]


def vector_sum(v1: Vector, v2: Vector) -> Vector:
    return v1[0] + v2[0], v1[1] + v2[1]


def scalar_prod(k: int, v: Vector) -> Vector:
    return k * v[0], k * v[1]


class DiophantineSolver:

    def get_beizout_coeff(self, r0: int, r1: int) -> Tuple[int, int]:
        invert = False
        if r0 < r1:
            invert = True
            r0, r1 = r1, r0
        t0, t1 = 1, 0
        s0, s1 = 0, 1
        while r1 > 0:
            r2 = r0 % r1
            q = r0 // r1
            s2 = s0 - q * s1
            t2 = t0 - q * t1
            r0, r1 = r1, r2
            s0, s1 = s1, s2
            t0, t1 = t1, t2
        if invert:
            s0, t0 = t0, s0
        return t0, s0

    def get_solution_space(self, a: int, b: int, c: int) -> Tuple[Vector, Vector] | None:
        d = math.gcd(a, b)
        if c % d != 0:
            return None
        a = a // d
        b = b // d
        c = c // d
        u, z = self.get_beizout_coeff(a, b)
        # u * a + b * z = 1
        # u * a * c + b * z * c = c
        if u * a + b * z != 1:
            raise Exception(f"asdf for {a}, {b}")

        s = (u * c, z * c)
        v = (-1 * b, a)

        if s[1] > 0:
            k = s[1] // v[1]
            s = vector_sum(s, scalar_prod(-1 * k, v))
        elif s[1] < 0:
            k = abs(s[1]) // v[1]
            if abs(s[1]) % v[1] != 0:
                k += 1
            s = vector_sum(s, scalar_prod(k, v))

        # Check is min
        if min(s) >= 0:
            ts = vector_sum(s, scalar_prod(-1, v))

            if min(ts) >= 0:
                print(s, v, ts)
                input()
                raise Exception("*******")

        return s, v

    def iter_all_solutions(self, a: int, b: int, c: int) -> Generator[Tuple[int, int], None, None]:
        res = self.get_solution_space(a, b, c)
        if res is None:
            return
        s, v = res
        if min(s) < 0:
            return
        yield s
        while True:
            s = vector_sum(s, v)
            if s[0] >= 0 and s[1] >= 0:
                yield s
            else:
                break

    def solve(self, a: int, b: int, c: int) -> Set[Tuple[int, int]]:
        return set(self.iter_all_solutions(a, b, c))


class SolutionRetriever:

    def __init__(self):
        self.diophantine_solver = DiophantineSolver()

    def get_best_solution(
        self, space_1: Tuple[Vector, Vector], space_2: Tuple[Vector, Vector]
    ) -> Tuple[int, int] | None:
        s1, v1 = space_1
        s2, v2 = space_2
        # s1 + A * v1 = s2 + B * v2
        # A * v1 - B * v2 = s2 - s1
        s = vector_sum(s2, scalar_prod(-1, s1))
        # A * v1 - B * v2 = s
        dres = self.diophantine_solver.get_solution_space(v1[1], v2[1], s[1])
        if dres is None:
            return None
        p, d = dres
        # (A, - B) = p + L * d
        # A = p[0] + L * d[0]
        # - B = p[1] + L * d[1]
        # A * v1[0] - B * v2[0] = s[0]
        # (p[0] + L * d[0]) * v1[0] + (p[1] + L * d[1]) * v2[0] = s[0]
        # L * (d[0] * v1[0] + d[1] * v2[0]) = s[0] - p[0] * v1[0] - p[1] * v2[0]
        q = d[0] * v1[0] + d[1] * v2[0]
        m = s[0] - p[0] * v1[0] - p[1] * v2[0]
        if m % q != 0:
            return None
        l = m // q
        a = p[0] + l * d[0]
        b = p[1] + l * d[1]
        sol = vector_sum(s1, scalar_prod(a, v1))
        if sol != vector_sum(s2, scalar_prod(-1 * b, v2)):
            raise Exception("Sanity check failed")
        return sol


class Solver:

    def __init__(self):
        self.machines: List[Machine] = []
        self.diophantine_solver = DiophantineSolver()
        self.solution_retriever = SolutionRetriever()

    def _parse_value(self, line: str) -> Tuple[int, int]:
        raw = line.split(": ", maxsplit=1)[1].split(", ")
        return tuple(int(el[2:]) for el in raw)

    def parse(self, path: str) -> None:
        with open(path) as hand:
            lines = hand.readlines()
            i = 0
            while i < len(lines):
                button_a = self._parse_value(lines[i])
                button_b = self._parse_value(lines[i + 1])
                prize = self._parse_value(lines[i + 2])
                self.machines.append(Machine(button_a=button_a, button_b=button_b, prize=prize))
                i += 4

    def _solve(self, increase: int = 0) -> int:
        tokens = 0
        for machine in self.machines:
            space_x = self.diophantine_solver.get_solution_space(
                machine.button_a[0], machine.button_b[0], machine.prize[0] + increase
            )
            if space_x is None:
                continue
            space_y = self.diophantine_solver.get_solution_space(
                machine.button_a[1], machine.button_b[1], machine.prize[1] + increase
            )
            if space_y is None:
                continue
            best_solution = self.solution_retriever.get_best_solution(space_x, space_y)
            if best_solution is None:
                continue
            tokens += 3 * best_solution[0] + best_solution[1]
        return tokens

    def solve1(self) -> int:
        tokens = 0
        for machine in self.machines:
            solve_x = self.diophantine_solver.solve(machine.button_a[0], machine.button_b[0], machine.prize[0])
            solve_y = self.diophantine_solver.solve(machine.button_a[1], machine.button_b[1], machine.prize[1])
            valid_solutions = solve_x & solve_y
            best_cost = None
            for solution in valid_solutions:
                if max(solution) > 100:
                    continue
                cost = 3 * solution[0] + solution[1]
                if best_cost is None or cost < best_cost:
                    best_cost = cost
            if best_cost is not None:
                tokens += best_cost
        return tokens

    def solve2(self) -> int:
        increase = 10000000000000
        tokens = 0
        for machine in self.machines:
            space_x = self.diophantine_solver.get_solution_space(
                machine.button_a[0], machine.button_b[0], machine.prize[0] + increase
            )
            if space_x is None:
                continue
            space_y = self.diophantine_solver.get_solution_space(
                machine.button_a[1], machine.button_b[1], machine.prize[1] + increase
            )
            if space_y is None:
                continue
            best_solution = self.solution_retriever.get_best_solution(space_x, space_y)
            if best_solution is None:
                continue
            tokens += 3 * best_solution[0] + best_solution[1]
        return tokens


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
