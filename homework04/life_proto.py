# type: ignore
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []

        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = 0
                row.append(cell_value)

            grid.append(row)

        return grid

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color = "green" if self.grid[i][j] == 1 else "white"
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # Исключаем текущую клетку из списка соседей
                if (i, j) != cell:
                    # Проверяем, чтобы сосед не выходил за границы поля
                    if 0 <= i < self.cell_height and 0 <= j < self.cell_width:
                        neighbours.append((i, j))

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0] * self.cell_width for _ in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
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


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
