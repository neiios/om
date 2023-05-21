import numpy as np


class TableRow:
    def __init__(self, cf: [float], fval: float):
        self.cf = cf
        self.fval = fval

    def __str__(self) -> str:
        return f"{self.cf}, {self.fval}"


def pivoting(index: int, full_table: [TableRow]) -> int:
    ratios = []

    for row in full_table[1:]:
        if row.cf[index] == 0:
            ratio = float("inf")
        else:
            ratio = row.fval / row.cf[index]
        ratios.append(ratio)

    print(f"Ratios: {ratios}")

    # Increment by one because of the function row in the table
    # TODO BUG: wtf should i do when x == -0.0 (if works in this case)
    return ratios.index(min([x for x in ratios if x >= 0])) + 1


def adjust_table(
    full_table: [TableRow], pivot_row_index: int, pivot_col_index: int
) -> None:
    pivot = full_table[pivot_row_index].cf[pivot_col_index]

    # Divide each element in the pivot row by the pivot.
    # Pivot element should become 1.
    pivot_row = full_table[pivot_row_index]
    pivot_row.fval = pivot_row.fval / pivot
    pivot_row.cf = [x / pivot for x in pivot_row.cf]

    for row in full_table:
        print(row)
    print("---------")

    for i in range(len(full_table)):
        if i == pivot_row_index:
            continue

        same_col_as_pivot_el = full_table[i].cf[pivot_col_index]
        new_pivot = full_table[pivot_row_index].cf[pivot_col_index]
        ratio = same_col_as_pivot_el / new_pivot
        print(f"Ratio: {ratio}")

        full_table[i].cf = [
            x - ratio * pivot_row_el
            for x, pivot_row_el in zip(full_table[i].cf, pivot_row.cf)
        ]

        full_table[i].fval = full_table[i].fval - ratio * pivot_row.fval

    for row in full_table:
        print(row)


def optimize_linear_program(full_table: [TableRow]) -> None:
    print("Finding an optimal solution:")

    function_row = full_table[0]
    # Loop until there are no negative values in the function row
    while not all(num >= 0 for num in function_row.cf):
        print("Current table:")
        for row in full_table:
            print(row)

        pivot_col_index = np.argmin(function_row.cf)
        print(f"Smallest objective function coefficient: {pivot_col_index}")

        pivot_row_index = pivoting(pivot_col_index, full_table)
        print(f"Smallest non-negative ratio index: {pivot_row_index}")

        pivot = full_table[pivot_row_index].cf[pivot_col_index]
        print(f"Pivot: {pivot}")

        adjust_table(full_table, pivot_row_index, pivot_col_index)

        input("Stopped execution. Press any button to continue.")


def main() -> None:
    # We have 7 variables in total. 4 are given and 3 are slack.
    # Left most element of the list is a constant.
    # First row must be an objective function.
    task = [
        TableRow([2, -3, 0, -5, 0, 0, 0], 0),  # <- Objective function
        TableRow([-1, 1, -1, -1, 1, 0, 0], 8),  # <- Constraints
        TableRow([2, 4, 0, 0, 0, 1, 0], 10),
        TableRow([0, 0, 1, 1, 0, 0, 1], 3),
    ]

    task = [
        TableRow([2, -3, 0, -5, 0, 0, 0], 0),  # <- Objective function
        TableRow([-1, 1, -1, -1, 1, 0, 0], 0),  # <- Constraints
        TableRow([2, 4, 0, 0, 0, 1, 0], 3),
        TableRow([0, 0, 1, 1, 0, 0, 1], 9),
    ]

    optimize_linear_program(task)


if __name__ == "__main__":
    main()
