# type: ignore
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = 0
                row.append(cell_value)

            grid.append(row)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell[0], cell[1]
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < len(self.curr_generation) and 0 <= j < len(self.curr_generation[0]):
                    if (i, j) != (row, col):
                        neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        next_generation = [[0] * self.cols for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = sum(self.get_neighbours((row, col)))
                cell = self.curr_generation[row][col]
                if (cell == 1 and 2 <= neighbours <= 3) or (cell == 0 and neighbours == 3):
                    next_generation[row][col] = 1
                else:
                    next_generation[row][col] = 0
        self.curr_generation = next_generation.copy()
        return next_generation

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation is not None and self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as file:
            lines = file.readlines()

        # Извлекаем размеры сетки из первой строки файла
        size = (len(lines), len(lines[0].strip()))

        # Создаем объект GameOfLife с указанными размерами
        game = GameOfLife(size, randomize=False)

        # Инициализируем сетку значениями из файла
        game.grid = [[int(char) for char in line.strip()] for line in lines]

        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as file:
            for row in self.curr_generation:
                line = "".join(map(str, row))
                file.write(f"{line}\n")
