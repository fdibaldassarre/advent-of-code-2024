#!/usr/bin/env python
import collections
from typing import List, Deque


class Memory:

    def __init__(self, a: int, b: int, c: int, instructions: List[int]) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.instructions = instructions


class Instruction:

    opcode = -1

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def get_operand_combo(self, value: int) -> str:
        if value <= 3:
            return str(value)
        elif value == 4:
            return "A"
        elif value == 5:
            return "B"
        elif value == 6:
            return "C"
        else:
            raise Exception("Unexpected operand 7")

    def get_combo_operand_value(self, value: int) -> int:
        if value <= 3:
            return value
        elif value == 4:
            return self.memory.a
        elif value == 5:
            return self.memory.b
        elif value == 6:
            return self.memory.c
        else:
            raise Exception("Unexpected operand 7")

    def run(self, pointer: int) -> int:
        if self.memory.instructions[pointer] != self.opcode:
            raise Exception("Unexpected value")
        return self.execute(pointer)

    def execute(self, pointer: int) -> int:
        raise NotImplementedError("Not implemented")

    def print(self, pointer: int) -> None:
        raise NotImplementedError("Not implemented")


class DivInstruction(Instruction):

    def divide(self, pointer) -> int:
        operand = self.memory.instructions[pointer + 1]
        num = self.memory.a
        den = 2 ** self.get_combo_operand_value(operand)
        return num // den

    def get_division(self, pointer: int) -> str:
        operand = self.memory.instructions[pointer + 1]
        return f"A // (2 ^ {self.get_operand_combo(operand)})"


class AdvInstruction(DivInstruction):

    opcode = 0

    def execute(self, pointer: int) -> int:
        self.memory.a = self.divide(pointer)
        return pointer + 2

    def print(self, pointer: int) -> None:
        print(f"A = {self.get_division(pointer)}")


class BxlInstruction(Instruction):
    opcode = 1

    def execute(self, pointer: int) -> int:
        operand = self.memory.instructions[pointer + 1]
        self.memory.b = self.memory.b ^ operand
        return pointer + 2

    def print(self, pointer: int) -> None:
        operand = self.memory.instructions[pointer + 1]
        print(f"B = B ^ {self.get_operand_combo(operand)}")


class BstInstruction(Instruction):
    opcode = 2

    def execute(self, pointer: int) -> int:
        operand = self.memory.instructions[pointer + 1]
        value = self.get_combo_operand_value(operand)
        self.memory.b = value % 8
        return pointer + 2

    def print(self, pointer: int) -> None:
        operand = self.memory.instructions[pointer + 1]
        print(f"B = {self.get_operand_combo(operand)} % 8")


class JnzInstruction(Instruction):
    opcode = 3

    def execute(self, pointer: int) -> int:
        if self.memory.a == 0:
            return pointer + 2
        operand = self.memory.instructions[pointer + 1]
        return operand

    def print(self, pointer: int) -> None:
        print("Jump or exit")


class BxcInstruction(Instruction):
    opcode = 4

    def execute(self, pointer: int) -> int:
        self.memory.b = self.memory.b ^ self.memory.c
        return pointer + 2

    def print(self, pointer: int) -> None:
        print(f"B = B ^ C")


class OutInstruction(Instruction):
    opcode = 5

    def __init__(self, memory: Memory, out: Deque[int]) -> None:
        super().__init__(memory)
        self.out = out

    def execute(self, pointer: int) -> int:
        operand = self.memory.instructions[pointer + 1]
        value = self.get_combo_operand_value(operand) % 8
        self.out.append(value)
        return pointer + 2

    def print(self, pointer: int) -> None:
        operand = self.memory.instructions[pointer + 1]
        print(f"Sys.Out: {self.get_operand_combo(operand)} % 8")


class BdvInstruction(DivInstruction):
    opcode = 6

    def execute(self, pointer: int) -> int:
        self.memory.b = self.divide(pointer)
        return pointer + 2

    def print(self, pointer: int) -> None:
        print(f"B = {self.get_division(pointer)}")


class CdvInstruction(DivInstruction):
    opcode = 7

    def execute(self, pointer: int) -> int:
        self.memory.c = self.divide(pointer)
        return pointer + 2

    def print(self, pointer: int) -> None:
        print(f"C = {self.get_division(pointer)}")


class Interpreter:

    def __init__(self, registers: List[int], instructions: List[int]) -> None:
        self.memory = Memory(*registers, instructions=instructions)
        self.out = collections.deque()
        self.pointer = 0
        self.instructions = [
            AdvInstruction(self.memory),
            BxlInstruction(self.memory),
            BstInstruction(self.memory),
            JnzInstruction(self.memory),
            BxcInstruction(self.memory),
            OutInstruction(self.memory, self.out),
            BdvInstruction(self.memory),
            CdvInstruction(self.memory),
        ]

    def run(self) -> None:
        while self.pointer < len(self.memory.instructions):
            iid = self.memory.instructions[self.pointer]
            instruction = self.instructions[iid]
            self.pointer = instruction.execute(self.pointer)

    def print(self) -> None:
        while self.pointer < len(self.memory.instructions):
            iid = self.memory.instructions[self.pointer]
            instruction = self.instructions[iid]
            instruction.print(self.pointer)
            self.pointer += 2

    def run_expecting(self, values: List[int]) -> bool:
        expected = 0
        while self.pointer < len(self.memory.instructions) and expected < len(values):
            iid = self.memory.instructions[self.pointer]
            instruction = self.instructions[iid]
            self.pointer = instruction.execute(self.pointer)
            if iid == OutInstruction.opcode:
                actual = self.out.pop()
                if actual == values[expected]:
                    expected += 1
                else:
                    break
        return expected == len(values)


class Solver:

    def __init__(self):
        self.registers = [0] * 3
        self.instructions = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for i in range(3):
                line = hand.readline().strip()
                self.registers[i] = int(line[12:])
            hand.readline()
            line = hand.readline().strip()[9:]
            self.instructions = [int(el) for el in line.split(",")]

    def solve1(self) -> str:
        interpreter = Interpreter(self.registers, instructions=self.instructions)
        interpreter.run()
        return ",".join([str(el) for el in interpreter.out])

    def solve2(self) -> int:
        valid_a = [0]
        for i in range(len(self.instructions)):
            target = self.instructions[len(self.instructions) - i - 1]
            new_valid_a = []
            for a in valid_a:
                for j in range(8):
                    candidate = a * 8 + j
                    interpreter = Interpreter([candidate, 0, 0], instructions=self.instructions)
                    interpreter.run()
                    res = list(interpreter.out)
                    if res[0] == target:
                        new_valid_a.append(candidate)
            valid_a = new_valid_a
        return min(valid_a)


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %s" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
