import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.cols = life.cols * self.cell_size
        self.rows = life.rows * self.cell_size
        self.screen = pygame.display.set_mode((life.cols * cell_size, life.rows * cell_size))
        pygame.init()

    def draw_lines(self) -> None:
        for x in range(0, self.cols, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.rows))
        for y in range(0, self.rows, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.cols, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = "green" if self.life.grid[i][j] == 1 else "white"
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                row, col = event.pos[1] // self.cell_size, event.pos[0] // self.cell_size
                self.life.curr_generation[row][col] = 1 if self.life.curr_generation[row][col] == 0 else 0
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause = not self.pause

    def run(self) -> None:
        clock = pygame.time.Clock()
        self.pause = False

        while True:
            self.handle_events()

            if not self.pause:
                self.life.step()

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":
    life = GameOfLife((50, 50))
    gui = GUI(life)
    gui.run()
