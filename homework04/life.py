import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


# type: ignore
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
        self.grid = self.create_grid(randomize=True)

    def create_grid(self, randomize: bool = False) -> Grid:
        self.grid = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = 0
                row.append(cell_value)

            self.grid.append(row)

        return self.grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # Исключаем текущую клетку из списка соседей
                if (i, j) != cell:
                    # Проверяем, чтобы сосед не выходил за границы поля
                    if 0 <= i < self.rows and 0 <= j < self.cols:
                        neighbours.append((i, j))

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                current_cell = (i, j)
                current_state = self.grid[i][j]
                neighbours = self.get_neighbours(current_cell)
                live_neighbours = sum(self.grid[x][y] for x, y in neighbours)

                if current_state == 1 and live_neighbours < 2:
                    new_grid[i][j] = 0  # Мертвая от перенаселения
                elif current_state == 1 and live_neighbours > 3:
                    new_grid[i][j] = 0  # Мертвая от одиночества
                elif current_state == 0 and live_neighbours == 3:
                    new_grid[i][j] = 1  # Рождение новой клетки
                else:
                    new_grid[i][j] = current_state  # Состояние остается неизменным

        self.grid = new_grid
        return self.grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation is not None and self.grid != self.prev_generation

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
            for row in self.grid:
                line = "".join(map(str, row))
                file.write(f"{line}\n")
