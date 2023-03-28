import numpy as np
import matplotlib.pyplot as plt
import pprint as pprint


def gradf(x):
    y1 = -(x[1] * (-2 * x[0] - x[1] + 1)) / 8
    y2 = -(x[0] * (1 - x[0] - 2 * x[1])) / 8
    return np.array([y1, y2])


def create_3d_plot(f, sp, filename: str) -> None:
    # Create a grid of x1 and x2 values
    x1_values = np.linspace(0, 1, 20)
    x2_values = np.linspace(0, 1, 20)
    x1, x2 = np.meshgrid(x1_values, x2_values)

    # Calculate the function values for each point in the grid
    z = f((x1, x2))

    # Plot the function as a 3D surface plot with a gradient
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x1,
                           x2,
                           z,
                           rstride=1,
                           cstride=1,
                           cmap='viridis',
                           edgecolor='none',
                           linewidth=0,
                           zorder=0)

    # Add the points in sp to the plot as red circles
    sp_x1, sp_x2 = zip(*sp)
    sp_z = f((np.array(sp_x1), np.array(sp_x2)))
    ax.scatter3D(sp_x1,
                 sp_x2,
                 sp_z,
                 c='r',
                 marker='o',
                 s=100,
                 alpha=1,
                 zorder=10)

    for i, point in enumerate(sp):
        ax.text(point[0],
                point[1],
                f(point) + 0.01,
                f'P{i+1}',
                color='black',
                fontsize=10,
                fontweight='bold')

    # Set the plot title and axis labels
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('fx')

    ax.view_init(30, 245)
    plt.savefig(filename)
    plt.show()


def print_results_old(f, steps, x, function_name: str) -> None:
    print(function_name)
    print(f'Starting point: {steps.pop(0)}')
    print("List of values the algorithm calculated:")
    for step in steps:
        print(f'{step}')

    print("-----------------")
    print(
        f'The algorithm made {len(steps)} steps, the function was called {len(steps)*2} times,\nthe final point is {x},\nvalue of the function at this point is {f(x)}'
    )
    print("--------------------------------------------------------")


def print_results(function_uses: int,
                  history: list,
                  res,
                  iterations: int,
                  additional_task_stats: dict = {}) -> None:
    print(f'Objective function was used {function_uses} times.')
    print(f'Objective function made {iterations} iterations.')
    print(f'Algorithm\'s results:')
    pprint.pprint(res)

    if 'iterations' and 'function_uses' and 'count' in additional_task_stats:
        print(
            f'Algorithm used {additional_task_stats["count"]} additional tasks.'
        )
        print(
            f'Additional tasks did {additional_task_stats["iterations"]} iterations in total.'
        )
        print(
            f'Additional tasks used the objective function {additional_task_stats["function_uses"]} times.'
        )

    print("History:")
    for point in history:
        pprint.pprint(point)
