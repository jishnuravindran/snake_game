import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QTimer

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE


class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake Game - PyQt6")
        self.setFixedSize(WIDTH, HEIGHT)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)

        self.reset_game()

    def reset_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.spawn_food()
        self.timer.start(120)

    def spawn_food(self):
        while True:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if food not in self.snake:
                self.food = food
                break

    def update_game(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            self.update()
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            self.update()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Background
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Snake
        painter.setBrush(QColor(0, 220, 0))
        for x, y in self.snake:
            painter.drawRect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

        # Food
        painter.setBrush(QColor(220, 30, 30))
        painter.drawEllipse(
            self.food[0] * CELL_SIZE,
            self.food[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        # Score
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 12))
        painter.drawText(10, 20, f"Score: {self.score}")

        if self.game_over:
            painter.setFont(QFont("Arial", 20))
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "GAME OVER\n\nPress R to Restart"
            )

    def keyPressEvent(self, event):
        key = event.key()

        if self.game_over:
            if key == Qt.Key.Key_R:
                self.reset_game()
            return

        if key == Qt.Key.Key_Up and self.direction != (0, 1):
            self.direction = (0, -1)

        elif key == Qt.Key.Key_Down and self.direction != (0, -1):
            self.direction = (0, 1)

        elif key == Qt.Key.Key_Left and self.direction != (1, 0):
            self.direction = (-1, 0)

        elif key == Qt.Key.Key_Right and self.direction != (-1, 0):
            self.direction = (1, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    game = SnakeGame()
    game.show()

    sys.exit(app.exec())