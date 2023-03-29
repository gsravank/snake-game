import pygame
import random
from enum import Enum
from collections import namedtuple

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x', 'y')

BLOCK_SIZE = 20

pygame.init()

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
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
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


    def play_step(self):
        pass



if __name__ == "__main__":
    game = SnakeGame()

    # game loop
    while True:
        game.play_step()

        # break if game is over

    pygame.quit()