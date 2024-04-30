# type: ignore
import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for y, row in enumerate(self.life.curr_generation):
            for x, val in enumerate(row):
                screen.addch(y + 1, x + 1, ord("*") if val == 1 else ord(" "))
        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)  # Скрываем курсор

        try:
            while not self.life.is_max_generations_exceeded and not self.life.is_changing:
                screen.clear()
                self.draw_borders(screen)
                curses.delay_output(200)
                screen.scrollok(True)
                self.draw_grid(screen)
                self.life.step()
                screen.refresh()

        finally:
            curses.endwin()


if __name__ == "__main__":
    # life = GameOfLife((, 80), max_generations=50)
    life = GameOfLife.from_file("glider.txt")
    ui = Console(life)
    ui.run()
