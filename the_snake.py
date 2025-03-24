"""Snake ver 0.99 beta Developed by Enot(c)"""

from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет отрисовки drow
DROW_COLOR = 4

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь управления движениями
MOVEMENT = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Snake ver 0.99 beta Developed by Enot(c)')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов — например, эти атрибуты
    описывают позицию и цвет объекта.
    Этот же класс содержит и заготовку метода для отрисовки объекта на игровом
     поле — draw.
    """

    def __init__(self):
        """Инициализирует базовые атрибуты класса - позицию и цвет."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self, surface: pygame.Surface):
        """Заготовка для отрисовки объектов"""


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко и
    действия с ним. Яблоко должно отображаться в случайных клетках
    игрового поля.
    """

    def __init__(self, occupied_cell=[]):
        """Инициализирует базовые атрибуты объекта, такие как его позиция
        и цвет.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_cell)

    def randomize_position(self, occupied_cell):
        """Устанавливает случайное положение яблока на игровом поле — задаёт
        атрибуту position новое значение.
        Координаты выбираются так, чтобы яблоко оказалось в пределах игрового
        поля.
        """
        while True:
            x_line = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_line = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x_line, y_line) not in occupied_cell:
                break
        return x_line, y_line

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, DROW_COLOR)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject, описывающий змейку и её
    поведение. Этот класс управляет её движением, отрисовкой,
    также обрабатывает действия пользователя.
    """

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.reset()

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя последний
         элемент, если длина змейки не увеличилась.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        xd, yd = self.direction
        self.positions.insert(0,
                              ((head_x + GRID_SIZE * xd) % SCREEN_WIDTH,
                               (head_y + GRID_SIZE * yd) % SCREEN_HEIGHT))

        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self):
        """Метод отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, DROW_COLOR)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key in MOVEMENT:
                snake.update_direction(MOVEMENT[event.key])


def main():
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(occupied_cell=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() == apple.position:
            snake.positions.append(snake.last)
            apple.position = apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
