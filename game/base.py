import pygame.draw

from settings import WIN_HEIGHT, WIN_WIDTH


class Base:
    def draw(self, win):
        floor_y = WIN_HEIGHT * 0.85
        pygame.draw.rect(win, (222, 184, 135), (0, floor_y, WIN_WIDTH, WIN_HEIGHT - floor_y))

        base_img = pygame.image.load("assets/base.png").convert()
        base = pygame.transform.scale(base_img, (WIN_WIDTH, WIN_HEIGHT - floor_y))

        win.blit(base, (0, floor_y))