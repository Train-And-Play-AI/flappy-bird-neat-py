import pygame.draw

from settings import WIN_WIDTH, WIN_HEIGHT

pygame.init()
STAT_FONT = pygame.font.SysFont(None, 30)

def draw_window(win, birds, pipes, base, score, highest_score, generation, from_watcher = False) :

    bg_img = pygame.image.load("assets/background-day.png").convert()
    bg = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))

    win.blit(bg, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)

    base.draw(win)

    score_ren = STAT_FONT.render("Score: " + str(score), True, (0, 0, 0))
    highest_score_ren = STAT_FONT.render("Highest Score: " + str(highest_score), True, (0, 0, 0))
    gen_ren = STAT_FONT.render("Gen: " + str(generation), True, (0, 0, 0))
    bird_alive_ren = STAT_FONT.render("Birds Alive: " + str(len(birds)), True, (0, 0, 0))

    win.blit(score_ren, (WIN_WIDTH - score_ren.get_width() - 10, 10))

    if not from_watcher :
        win.blit(highest_score_ren, (10, 10))
        win.blit(gen_ren, (10, 30))
        win.blit(bird_alive_ren, (10, 50))

    pygame.display.update()
