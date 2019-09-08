#!/usr/bin/env python3

__all__ = ["solve"]

def iter_possibilities(length, counts):
    if not counts:
        yield "." * length
    else:
        this_run, *rest = counts
        min_rest_len = len(counts) + sum(counts) - 1
        for offset in range(0, 1 + length - min_rest_len):
            lane = []
            lane.append("." * offset)
            lane.append("#" * this_run)
            if rest:
                lane.append(".")
            lane_segment = "".join(lane)
            for rest_of_lane in iter_possibilities(length - len(lane_segment), rest):
                yield lane_segment + rest_of_lane


def list_possibilities(length, counts):
    return list(iter_possibilities(length, counts))


def iter_lane_truth(possibilities):
    possibilities = list(possibilities)
    length = len(possibilities[0])
    for i in range(length):
        if all(possibility[i] == '#' for possibility in possibilities):
            yield '#'
        elif not any(possibility[i] == '#' for possibility in possibilities):
            yield '.'
        else:
            yield '?'

def lane_truth(possibilities):
    return "".join(iter_lane_truth(possibilities))

def iter_eliminate_impossibilities(truth, possibilities):
    for possibility in possibilities:
        keep = True
        for i, value in enumerate(truth):
            if value == '?':
                continue
            elif value != possibility[i]:
                keep = False
                break
        if keep:
            yield possibility

def eliminate_impossibilities(truth, possibilities):
    return list(iter_eliminate_impossibilities(truth, possibilities))


def combine_truths_into_row(i, row_truth, column_truths):
    new_row_truths = []
    for (truth, col) in zip(row_truth, column_truths):
        if truth == '?':
            new_row_truths.append(col[i])
        else:
            new_row_truths.append(truth)
    return ''.join(new_row_truths)


def combine_truths(row_truths, column_truths):
    return [
        combine_truths_into_row(i, row_truth, column_truths)
        for i, row_truth in enumerate(row_truths)
    ]

def count_unknown(truths):
    return sum(truth.count("?") for truth in truths)

def solve(rows, columns):
    """ Solve a picross / nonogram puzzle
    rows:  a sequence of sequences of counts for a the puzzle rows
    columns: a sequence of counts for the puzzle columns

    returns: a sequence of strings representing the rows of the solution
     '.' - not filled
     '#' - filled
    >>> solve(
            [[5], [5, 2], [4, 4], [2, 2, 5], [4, 1, 2, 2], [4, 2, 5], [5, 1, 6], [6, 6], [2, 8], [5], [5], [7], [7], [15], [15]],
            [[3, 2], [5, 2], [6, 2], [2, 5, 2], [3, 2, 4], [4, 8], [5, 9], [2, 1, 7], [1, 3, 8], [3, 9], [3, 4, 4], [3, 4, 2], [7, 2], [4, 2], [2, 2]])

    ['....#####......',
     '...#####..##...',
     '...####..####..',
     '.##..##.#####..',
     '####..#.##..##.',
     '####...##.#####',
     '#####.#..######',
     '.######.######.',
     '..##.########..',
     '.....#####.....',
     '.....#####.....',
     '....#######....',
     '....#######....',
     '###############',
     '###############']
    """


    row_possibilities = [
        list_possibilities(len(columns), row)
        for row in rows
    ]
    row_truths = [ "?" * len(columns) ] * len(rows)
    column_possibilities = [
        list_possibilities(len(rows), column)
        for column in columns
    ]
    column_truths = [ "?" * len(rows) ] * len(columns)

    unknown = count_unknown(row_truths)
    last_unknown = unknown + 1 # make it one more so that it will run_once

    while unknown < last_unknown:
        last_unknown = unknown
        row_possibilities = [
            eliminate_impossibilities(truth, possibilities)
            for truth, possibilities in zip(row_truths, row_possibilities)
        ]

        row_truths = [
            lane_truth(possibilities)
            for possibilities in row_possibilities
        ]

        column_truths = combine_truths(column_truths, row_truths)

        column_possibilities = [
            eliminate_impossibilities(truth, possibilities)
            for truth, possibilities in zip(column_truths, column_possibilities)
        ]

        column_truths = [
            lane_truth(possibilities)
            for possibilities in column_possibilities
        ]

        row_truths = combine_truths(row_truths, column_truths)
        unknown = count_unknown(row_truths)

    return row_truths


def main():
    import sys
    import re
    COUNTS = re.compile("^\d+(\s*,\s*\d+)*$")
    columns = []
    rows = []
    current = columns

    for arg in sys.argv[1:]:
        arg = arg.strip()
        if arg == 'x' and current is columns:
            current = rows
        elif COUNTS.match(arg):
            counts = [int(x.strip()) for x in arg.split(",")]
            current.append(counts)
        else:
            print(f"Error: unexpeted input {arg!r}", file=sys.stderr)
            sys.exit(1)

    solution = solve(columns, rows)
    for row in solution:
        print(row)
    sys.exit(1)


if __name__ == "__main__":
    main()
