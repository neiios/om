import numpy as np
import matplotlib.pyplot as plt
import os

import nelder_mead as nm
import output as o
import descent_methods as dm


def f(x):
    return -0.125 * x[0] * x[1] * (1 - x[0] - x[1])


def gradf(x):
    y1 = -(x[1] * (-2 * x[0] - x[1] + 1)) / 8
    y2 = -(x[0] * (1 - x[0] - 2 * x[1])) / 8
    return np.array([y1, y2])


def main():
    a = 6
    b = 9
    starting_points = np.array([[0, 0], [1, 1], [a / 10, b / 10]])
    o.create_3d_plot(f, starting_points, "starting-points.png")

    for starting_point in starting_points:
        print("--------------------------------------------------------")
        print(f"Starting point is [{starting_point[0]}, {starting_point[1]}]")

        print(f"\nGradient descent:")
        history, res, function_uses = dm.gradient_descent(
            gradf, starting_point)
        o.print_results(function_uses, history, res, len(history) - 1)

        print(f"\nSteepest descent:")
        history, res, function_uses, stats_additional = dm.steepest_descent(
            f, gradf, starting_point)
        o.print_results(function_uses, history, res,
                        len(history) - 1, stats_additional)

        print(f"\nNelder-Mead:")
        res, history, function_uses = nm.nelder_mead(f, starting_point)
        o.print_results(function_uses, history, res, len(history))

        print("--------------------------------------------------------")

        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
