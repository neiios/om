from typing import Callable
from nelder_mead import nelder_mead, find_best_points_index
import numpy as np


def f(x: list[float]) -> float:
    return -1 * x[0] * x[1] * x[2]


def eq_constraint(x: list[float]) -> float:
    return 2 * (x[0] * x[1] + x[1] * x[2] + x[0] * x[2]) - 1


def ineq_constraint1(x: list[float]) -> float:
    return -1 * x[0]


def ineq_constraint2(x: list[float]) -> float:
    return -1 * x[1]


def ineq_constraint3(x: list[float]) -> float:
    return -1 * x[2]


def penalty(x: list[float], equality_constraints: list[Callable[[list[float]], float]],
            inequality_constraints: list[Callable[[list[float]], float]]) -> float:
    temp_sum = [0, 0]

    for equality_constraint in equality_constraints:
        temp_sum[0] += equality_constraint(x) ** 2

    for inequality_constraint in inequality_constraints:
        temp_sum[1] += max(0.0, inequality_constraint(x)) ** 2

    return temp_sum[0] + temp_sum[1]


def b(x: list[float], r: float, equality_constraints: list[Callable[[list[float]], float]],
      inequality_constraint: list[Callable[[list[float]], float]]):
    return f(x) + (1 / r) * penalty(x, equality_constraints, inequality_constraint)


def optimize(starting_point: list[float], equality_constraints: list[Callable[[list[float]], float]],
             inequality_constraints: list[Callable[[list[float]], float]]):
    r = 1
    total_function_calls = 0

    current_point = starting_point
    for i in range(1, 100):
        b_wrapped = lambda x: b(x, r, equality_constraints, inequality_constraints)
        simplex, _, function_calls = nelder_mead(b_wrapped, current_point)
        new_point = simplex[find_best_points_index(simplex)]["coords"]
        r = r / 2
        total_function_calls += function_calls

        if np.linalg.norm(new_point - current_point) <= 0.001:
            current_point = new_point
            break
        current_point = new_point

    return current_point, total_function_calls


def main():
    points = [[0, 0, 0], [1, 1, 1], [2 / 10, 6 / 10, 9 / 10]]
    eqc = [eq_constraint]
    ineqc = [ineq_constraint1, ineq_constraint2, ineq_constraint3]

    for point in points:
        print("----------------------------------")
        print(f"Pradinis taškas: {point}")
        print(f"Funkcijos reikšmė: {f(point)}")

        print(f"Lygibiniai apribojimai:")
        print(f"{eq_constraint(point)}")

        print(f"Nelygibiniai apribojimai:")
        print(f"{ineq_constraint1(point)}")
        print(f"{ineq_constraint2(point)}")
        print(f"{ineq_constraint3(point)}")

        print(f"Optimization: {optimize(point, eqc, ineqc)}")


if __name__ == "__main__":
    main()