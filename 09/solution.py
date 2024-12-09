#!/usr/bin/env python

import heapq


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, path: str) -> None:
        with open(path) as hand:
            self.data = hand.read().strip()

    def solve1(self) -> int:
        free_space_intervals = []
        heapq.heapify(free_space_intervals)
        files_intervals = []
        heapq.heapify(files_intervals)
        cur_idx = 0
        leftmost_free = len(self.data)
        rightmost_occupied = 0
        for i, el in enumerate(self.data):
            size = int(el)
            interval = (cur_idx, cur_idx + size)
            cur_idx += size
            if size == 0:
                continue
            if i % 2 == 0:
                file_id = i // 2
                heapq.heappush(files_intervals, (-1 * interval[0], -1 * interval[1], file_id))
                rightmost_occupied = max(rightmost_occupied, interval[1])
            else:
                leftmost_free = min(leftmost_free, interval[0])
                heapq.heappush(free_space_intervals, interval)

        while leftmost_free < rightmost_occupied:
            # Pick the right-most file
            right_file = heapq.heappop(files_intervals)
            right_start, right_end, file_id = right_file
            right_start = -1 * right_start
            right_end = -1 * right_end
            right_dim = right_end - right_start
            left_most_free = heapq.heappop(free_space_intervals)
            left_start, left_end = left_most_free
            left_dim = left_end - left_start

            # Split and move
            moved_size = min(right_dim, left_dim)
            moved_file = left_start, left_start + moved_size
            rem_free = moved_file[1], left_end

            rem_file = right_start, right_end - moved_size
            new_free_space = rem_file[1], right_end

            # Moved file
            heapq.heappush(files_intervals, (-1 * moved_file[0], -1 * moved_file[1], file_id))
            # Remainder file
            if rem_file[0] < rem_file[1]:
                heapq.heappush(files_intervals, (-1 * rem_file[0], -1 * rem_file[1], file_id))

            # Free space
            if rem_free[0] < rem_free[1]:
                heapq.heappush(free_space_intervals, rem_free)
            heapq.heappush(free_space_intervals, new_free_space)

            # Update leftmost and rightmost
            leftmost_free = free_space_intervals[0][0]
            rightmost_occupied = -1 * files_intervals[0][0]

        checksum = 0
        for interval in files_intervals:
            start, end, file_id = interval
            start = -1 * start
            end = -1 * end
            for c in range(start, end):
                checksum = checksum + c * file_id
        return checksum

    def solve2(self) -> int:
        free_space_intervals = []
        for _ in range(10):
            intervals = []
            heapq.heapify(intervals)
            free_space_intervals.append(intervals)

        files_intervals = []
        cur_idx = 0
        for i, el in enumerate(self.data):
            size = int(el)
            interval = (cur_idx, cur_idx + size)
            cur_idx += size
            if size == 0:
                continue
            if i % 2 == 0:
                files_intervals.append(interval)
            else:
                heapq.heappush(free_space_intervals[size], interval)

        files_intervals.reverse()

        moved_files_intervals = []
        for i, interval in enumerate(files_intervals):
            file_id = len(files_intervals) - i - 1
            size = interval[1] - interval[0]

            left_most = None
            for candidate in range(size, 10):
                if len(free_space_intervals[candidate]) == 0:
                    continue
                free_space = free_space_intervals[candidate][0]
                if interval[0] < free_space[0]:
                    # Interval is to the right of the file
                    continue
                if left_most is None or free_space[0] < left_most[0]:
                    left_most = free_space

            if left_most is None:
                # File does not move
                moved_files_intervals.append((interval, file_id))
            else:
                # Move to the free space
                free_start, free_end = left_most
                free_size = free_end - free_start

                new_file = free_start, free_start + size
                new_free = new_file[1], free_end
                new_free_size = new_free[1] - new_free[0]

                heapq.heappop(free_space_intervals[free_size])
                if new_free_size > 0:
                    heapq.heappush(free_space_intervals[new_free_size], new_free)
                moved_files_intervals.append((new_file, file_id))

        checksum = 0
        for file in moved_files_intervals:
            interval, file_id = file
            start, end = interval
            for c in range(start, end):
                checksum = checksum + c * file_id

        return checksum


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
