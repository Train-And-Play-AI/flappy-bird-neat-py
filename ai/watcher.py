import pickle
import pygame

import neat

from game.base import Base
from game.bird import Bird
from game.pipe import Pipe
from game.utils import draw_window
from settings import WIN_WIDTH, WIN_HEIGHT, PIPE_GAP

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
wing_sound = pygame.mixer.Sound("assets/sounds/wing.wav")
point_sound = pygame.mixer.Sound("assets/sounds/point.wav")

def play(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    bird = Bird(230, 300)

    pipes = [Pipe(500)]

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    score = 0
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + 30:
            pipe_ind = 1

        output = net.activate((
            bird.y,
            abs(bird.y - pipes[pipe_ind].y),
            abs(bird.y - pipes[pipe_ind].y + PIPE_GAP)))

        if output[0] > 0.5:
            bird.jump()
            pygame.mixer.Sound.play(wing_sound)

        bird.move()

        add_pipe = False
        rem = []



        for pipe in pipes:
            if pipe.collide(bird):
               run = False
               pygame.mixer.Sound.play(hit_sound)
            if not pipe.passed and pipe.x < bird.x:
                add_pipe = True
                pipe.passed = True
            pipe.move()

            if pipe.x + 30 < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pygame.mixer.Sound.play(point_sound)
            if score > 20:
                run = False
            pipes.append(Pipe(500))

        for r in rem:
            pipes.remove(r)

        draw_window(win, [bird], pipes, Base(), score, 0, 0, True)


def run_with_ai(config_file):

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file)

    with open('best-genome.pkl', 'rb') as best_genome_file:
        best_genome = pickle.load(best_genome_file)

        play(best_genome, config)
