import numpy as np

verbose = False


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

    if verbose:
        print(f"Ratios: {ratios}")

    # Increment by one because of the function row in the table.
    # Originally there was an >= sign here. But > works better and IDK why.
    return ratios.index(min([x for x in ratios if x > 0])) + 1


def adjust_table(
    full_table: [TableRow], pivot_row_index: int, pivot_col_index: int
) -> None:
    pivot = full_table[pivot_row_index].cf[pivot_col_index]

    # Divide each element in the pivot row by the pivot.
    # Pivot element should become 1.
    pivot_row = full_table[pivot_row_index]
    pivot_row.fval = pivot_row.fval / pivot
    pivot_row.cf = [x / pivot for x in pivot_row.cf]

    if verbose:
        for row in full_table:
            print(row)
        print("---------")

    for i in range(len(full_table)):
        if i == pivot_row_index:
            continue

        same_col_as_pivot_el = full_table[i].cf[pivot_col_index]
        new_pivot = full_table[pivot_row_index].cf[pivot_col_index]
        ratio = same_col_as_pivot_el / new_pivot
        if verbose:
            print(f"Ratio: {ratio}")

        full_table[i].cf = [
            x - ratio * pivot_row_el
            for x, pivot_row_el in zip(full_table[i].cf, pivot_row.cf)
        ]

        full_table[i].fval = full_table[i].fval - ratio * pivot_row.fval

    if verbose:
        for row in full_table:
            print(row)


def optimize_linear_program(full_table: [TableRow], var_count: int) -> None:
    function_row = full_table[0]

    while not all(num >= 0 for num in function_row.cf):
        if verbose:
            print("Current table:")
            for row in full_table:
                print(row)

        pivot_col_index = np.argmin(function_row.cf)
        if verbose:
            print(
                f"Smallest objective function coefficient (column index): {pivot_col_index}"
            )

        pivot_row_index = pivoting(pivot_col_index, full_table)
        if verbose:
            print(f"Smallest non-negative ratio index (row index): {pivot_row_index}")

        pivot = full_table[pivot_row_index].cf[pivot_col_index]
        if verbose:
            print(f"Pivot: {pivot}")

        adjust_table(full_table, pivot_row_index, pivot_col_index)

        if verbose:
            input("Waiting for input. Press any key...")

    column_sums = [
        sum(row.cf[i] for row in full_table) for i in range(len(full_table[0].cf))
    ]
    base_indexes = [index for index, value in enumerate(column_sums) if value == 1]

    final_vars = [0] * var_count

    for row in full_table[1:]:
        for i in base_indexes:
            if row.cf[i] == 1:
                final_vars[i] = row.fval

    return final_vars, [x + 1 for x in base_indexes], -function_row.fval


def print_results(res: [[float], [float], float], true_var_count: int):
    print(f"Point: {res[0][0:true_var_count]}")
    print(f"Base: {res[1]}")
    print(f"Optimum: {res[2]}")


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

    print("Optimizing the generic task:")
    print_results(optimize_linear_program(task, 7), 4)

    task_personal = [
        TableRow([2, -3, 0, -5, 0, 0, 0], 0),
        TableRow([-1, 1, -1, -1, 1, 0, 0], 2),
        TableRow([2, 4, 0, 0, 0, 1, 0], 6),
        TableRow([0, 0, 1, 1, 0, 0, 1], 9),
    ]

    print("Optimizing the personal task:")
    print_results(optimize_linear_program(task_personal, 7), 4)

    another_test = [
        TableRow([2, -3, 0, -5, 0, 0, 0], 0),
        TableRow([-1, 1, -1, -1, 1, 0, 0], 0),
        TableRow([2, 4, 0, 0, 0, 1, 0], 3),
        TableRow([0, 0, 1, 1, 0, 0, 1], 9),
    ]

    print("Optimizing the test task:")
    print_results(optimize_linear_program(another_test, 7), 4)


if __name__ == "__main__":
    main()
