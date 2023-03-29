import pygame
import random
from enum import Enum
from collections import namedtuple, deque, defaultdict

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 15
MIN_SPEED = SPEED
MAX_SPEED = 2 * SPEED

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.fond.SysFont('arial', 25)

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake") # title of the game
        self.clock = pygame.time.Clock() # to maintain a particular speed for the game

        # Init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2) # start in the middle of the display
        self.snake = deque([self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)])
        self.starting_length = len(self.snake)
        self.block_map = defaultdict(lambda : False)
        for pt in self.snake:
            self.block_map[pt] = True

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        # Get multiples of block size, but a random one between 0 and maximum - block_size
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

        return


    def _get_curr_direction(self):
        first = self.snake[0]
        self.snake.append(self.snake.popleft())
        second = self.snake[0]
        self.snake.appendleft(self.snake.pop())

        if second.y == first.y:
            if first.x < second.x:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        else:
            if first.y < second.y:
                return Direction.UP
            else:
                return Direction.DOWN

    def _are_opposites(self, d1, d2):
        if d1 == Direction.LEFT:
            return d2 == Direction.RIGHT
        elif d1 == Direction.RIGHT:
            return d2 == Direction.LEFT
        elif d1 == Direction.UP:
            return d2 == Direction.DOWN
        else:
            return d2 == Direction.UP

    def play_step(self):
        # Collect user input
        prev_direction = self.direction

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # Move snake
        if self._are_opposites(self._get_curr_direction(), self.direction):
            self.direction = prev_direction

        self._move(self.direction)
        self.snake.appendleft(self.head)

        # Check if game over
        # and quit if so
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        else:
            self.block_map[self.head] = True

        # Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            tail = self.snake.pop()
            self.block_map[tail] = False

        # Update UI and clock
        self._update_ui()
        self.clock.tick(self._get_curr_speed())

        # Return game over and score

        return game_over, self.score

    def _get_curr_speed(self):
        return SPEED
        curr_len = len(self.snake)
        init_len = self.starting_length
        inc_len = curr_len - init_len

        inc_speed = inc_len // 2

        new_speed = MIN_SPEED + inc_speed

        return min(MAX_SPEED, max(MIN_SPEED, new_speed))

    def _is_collision(self):
        # Hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return  True

        # Hits itself
        if self.block_map[self.head]:# in self.snake[1:]:
            return True

        return False


    def _move(self, direction):
        x, y = self.head.x, self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
        return

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + (0.2 * BLOCK_SIZE), pt.y + (0.2 * BLOCK_SIZE), 0.6 * BLOCK_SIZE, 0.6 * BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()
        return


if __name__ == "__main__":
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        # break if game is over
        if game_over:
            break

    print(f"Game over!\nFinal score: {score}")

    pygame.quit()