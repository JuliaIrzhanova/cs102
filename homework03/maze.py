import random
from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    choice = ["up", "right"]
    x, y = coord[0], coord[1]
    route = random.choice(choice)
    if route == "up":
        if x != 1:
            grid[x - 1][y] = " "
        elif y + 2 != len(grid[0]):
            grid[x][y + 1] = " "
    else:
        if y + 2 != len(grid[0]):
            grid[x][y + 1] = " "
        elif x != 1:
            grid[x - 1][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 != 0 and y % 2 != 0:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for i in empty_cells:
        grid = remove_wall(grid, i)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for x, row in enumerate(grid):
        if "X" in row:
            for y, _ in enumerate(row):
                if grid[x][y] == "X":
                    exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    cells = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == k:
                cells.append([i, j])
    for i in range(len(cells)):
        x, y = cells[i][0], cells[i][1]
        if y != 0:
            if grid[x][y - 1] == " ":
                grid[x][y - 1] = k + 1
            elif grid[x][y - 1] == 0:
                grid[x][y - 1] = k + 1
        if x != 0:
            if grid[x - 1][y] == " ":
                grid[x - 1][y] = k + 1
            elif grid[x - 1][y] == 0:
                grid[x - 1][y] = k + 1
        if y != len(grid) - 1:
            if grid[x][y + 1] == " ":
                grid[x][y + 1] = k + 1
            elif grid[x][y + 1] == 0:
                grid[x][y + 1] = k + 1
        if x != len(grid) - 1:
            if grid[x + 1][y] == " ":
                grid[x + 1][y] = k + 1
            elif  grid[x + 1][y] == 0:
                grid[x + 1][y] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    a, b = exit_coord[0], exit_coord[1]
    exit = grid[exit_coord[0]][exit_coord[1]]
    k = int(grid[a][b]) - 1
    path = []
    current = a, b
    path.append(current)
    while k != 0:
        if a + 1 < len(grid) and grid[a + 1][b] == k:
                current = a + 1, b
                a += 1
        if a - 1 >= 0 and grid[a - 1][b] == k:
                current = a - 1, b
                a -= 1
        if b + 1 < len(grid) and grid[a][b + 1] == k:
                current = a, b + 1
                b += 1
        if b - 1 >= 0 and grid[a][b - 1] == k:
                current = a, b - 1
                b -= 1
        path.append(current)
        k -= 1
    if len(path) != exit:
        x = path[-1][0]
        y = path[-1][1]
        grid[x][y] = " "
        p, q = path[-2][0], path[-2][1]
        shortest_path(grid, (p, q))
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == len(grid) - 1)
        or (x == len(grid) - 1 and y == 0)
        or (x == len(grid) - 1 and y == len(grid))
    ):
        return True
    if y == 0 and grid[x][y + 1] == "■":
        return True
    if y == len(grid) - 1 and grid[x][y - 1] == "■":
        return True
    if x == 0 and grid[x + 1][y] == "■":
        return True
    if x == len(grid) - 1 and grid[x - 1][y] == "■":
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    lnx = len(grid)
    lny = len(grid[0])
    coordinate = get_exits(grid)
    if len(coordinate) == 1:
        return grid, coordinate[0]
    if not encircled_exit(grid, coordinate[0]) and not encircled_exit(grid, coordinate[1]):
        for x in range(lnx):
            for y in range(lny):
                if grid[x][y] == " ":
                    grid[x][y] = 0
        grid[coordinate[0][0]][coordinate[0][1]] = 1
        grid[coordinate[1][0]][coordinate[1][1]] = 0
        k = 1
        while grid[coordinate[1][0]][coordinate[1][1]] == 0:
            grid = make_step(grid, k)
            k += 1
        route = shortest_path(grid, coordinate[1])
        for x in range(lnx):
            for y in range(lny):
                if grid[x][y] != " " and grid[x][y] != "■":
                    grid[x][y] = " "
        return grid, route
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                if str(grid[i][j]).isdigit():
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
