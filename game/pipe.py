import random

import pygame.draw

from settings import WIN_HEIGHT, PIPE_VELOCITY, PIPE_GAP


class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = random.randrange(150, int(WIN_HEIGHT * 0.85) - 150 - PIPE_GAP)
        self.passed = False

        self.pipe_top_img = pygame.image.load("assets/pipe-top-green.png")
        self.pipe_btm_img = pygame.image.load("assets/pipe-bottom-green.png")


    def draw(self, win):

        # Top Pipe
        top_pipe = pygame.transform.scale(self.pipe_top_img.convert(), (30, self.y))
        win.blit(top_pipe, (self.x, 0))

        # Bottom Pipe
        btm_pipe = pygame.transform.scale(self.pipe_btm_img.convert(), (30, WIN_HEIGHT))
        win.blit(btm_pipe, (self.x, self.y + PIPE_GAP))

    def move(self):
        self.x -= PIPE_VELOCITY

    def collide(self, bird):
        if bird.x + 10 > self.x and bird.x < self.x + 30 and (self.y > bird.y or self.y + PIPE_GAP < bird.y + 10):
            return True
        return False