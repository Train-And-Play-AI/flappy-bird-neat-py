import pygame

from settings import BIRD_VELOCITY, GRAVITY


class Bird:
    IMAGES = [
        pygame.image.load('assets/bluebird-downflap.png'),
        pygame.image.load('assets/bluebird-midflap.png'),
        pygame.image.load('assets/bluebird-upflap.png'),
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0

        self.img_idx = 0

    def draw(self, win):
        bird = pygame.transform.scale(self.IMAGES[self.img_idx].convert(), (20, 20))
        win.blit(bird, (self.x, self.y))


    def move(self):
        self.tick_count += 1
        displacement = BIRD_VELOCITY * self.tick_count + 0.5 * GRAVITY * self.tick_count ** 2

        if displacement > 10:
            displacement = 10

        if displacement < 0:
            displacement = -2

        self.y += displacement

    def jump(self):
        self.tick_count = 0
        self.img_idx = (self.img_idx + 1) % 3