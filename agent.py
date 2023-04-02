import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        return

    def get_state(self, game):
        return

    def remember(self, state, action, reward, next_state, done):
        return

    def train_long_memory(self):
        return

    def train_short_memory(self):
        return

    def get_action(self, state):
        return


def train():
    return


if __name__ == "__main__":
    train()