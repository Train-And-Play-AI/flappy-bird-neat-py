import pickle
import  pygame

import neat

from game.base import Base
from game.bird import Bird
from game.pipe import Pipe
from game.utils import draw_window
from settings import MAX_GEN, WIN_WIDTH, WIN_HEIGHT, PIPE_GAP


def eval_genome(genomes, config):
    global highest_score
    global  generation
    generation += 1

    nets =[]
    ge = []
    birds =[]

    pipes = [Pipe(500)]

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        bird = Bird(230, 300)
        birds.append(bird)

        genome.fitness = 0.0
        ge.append(genome)


        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()

        score = 0
        run =True

    while run  and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x  > pipes[0].x + 30:
            pipe_ind = 1


        for i, bird in enumerate(birds):
            bird.move()

            ge[i].fitness += 0.1

            output = nets[i].activate((
                bird.y,
                abs(bird.y - pipes[pipe_ind].y),
                abs(bird.y - pipes[pipe_ind].y + PIPE_GAP)))

            if output[0] > 0.5:
                bird.jump()


        add_pipe = False
        rem = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    continue

                if not pipe.passed and pipe.x < bird.x:
                    add_pipe = True
                    pipe.passed = True
            pipe.move()

            if pipe.x + 30 < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            if score > 20:
                run = False
                for g in ge:
                    g.fitness += 10000
            if score > highest_score:
                highest_score = score

            for g in ge:
                g.fitness += 5


            pipes.append(Pipe(500))

        for r in rem:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y + 10 > WIN_HEIGHT or bird.y + 10 < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        draw_window(win, birds, pipes, Base(), score, highest_score, generation)




def run_neat(config_file):
    global highest_score
    highest_score = 0

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    global generation
    generation = 0

    best_genome = pop.run(lambda genomes, config: eval_genome(genomes, config), MAX_GEN)

    with open('best-genome.pkl', 'wb') as best_genome_file:
        pickle.dump(best_genome, best_genome_file)
