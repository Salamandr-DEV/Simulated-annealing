import random
import numpy as np
import time
import matplotlib.pyplot as plt
import pygame

def Max_Fitnes(bord_size):
    max_fitnes = 0
    i = bord_size - 1
    while(i > 0):
        max_fitnes += i
        i -= 1
    return max_fitnes

def Random_solution(bord_size):
    result = []
    for i in range(bord_size):
        result.append(random.randint(0,bord_size-1))
    return result

def Fitnes(solution):
    conflicts = 0
    n = len(solution)
    for i in range(n):
        for j in range(i+1, n):
            if i != j:
                if solution[i] == solution[j]:
                    conflicts += 1
                if abs(solution[i] - solution[j]) == abs(i - j):
                    conflicts += 1
    return conflicts

def Mutate(x):
    neighbour = x[:]
    c = random.randint(0, len(neighbour) - 1)
    m = random.randint(0, len(neighbour) - 1)
    n = len(neighbour)
    neighbour[c] = m
    return neighbour

def draw(width, higth, best, size_player):
    background = pygame.Surface((width, higth))
    background.fill((255, 255, 255))
    player = pygame.transform.scale(pygame.image.load('Ферзь.png').convert(), (size_player, size_player))
    player.set_colorkey((47, 161, 142))

    LINE = (0, 0, 0)

    line = pygame.Surface((size_player, size_player))
    line.fill((107, 78, 88))

    for i in range(0, n + 1):
        if i % 2 == 0:
            for j in range(0, n + 1):
                if j % 2 == 1:
                    background.blit(line, ((i - 1) * size_player, (j - 1) * size_player))
        else:
            for j in range(0, n + 1):
                if j % 2 == 0:
                    background.blit(line, ((i - 1) * size_player, (j - 1) * size_player))

    for i in range(0, width, int(width / n)):
        pygame.draw.line(background, LINE, (i, 0), (i, higth), 1)
        #pygame.display.update()

    for i in range(0, higth, int(higth / n)):
        pygame.draw.line(background, LINE, (0, i), (width, i), 1)
        #pygame.display.update()

    for i in range(len(best)):
        y = ((n - best[i] - 1) * size_player)  # - (size_player/2)
        x = (i * size_player)  # - (size_player/2)
        # , int((WIN_HEIGHT/n)/4)
        background.blit(player, (int(x), int(y)))
        xd = int(x) + (size_player/2)
        yd = int(y) + (size_player/2)

        # pygame.draw.line(background, colour[i], (xd, yd), (int(xd - ((n - (n - best[i])) * size_player)), int(yd + ((n - (n - best[i])) * size_player))), 3)
        # pygame.draw.line(background, colour[i], (xd, yd), (int(xd + ((n - best[i]) * size_player)), int(yd - ((n - best[i]) * size_player))), 3)
        # pygame.draw.line(background, colour[i], (xd, yd), (int(xd - ((n - best[i]) * size_player)), int(yd - ((n - best[i]) * size_player))), 3)
        # pygame.draw.line(background, colour[i], (xd, yd), (int(xd + ((n - (n - best[i])) * size_player)), int(yd + ((n - (n - best[i])) * size_player))), 3)
    return background

if __name__ == "__main__":
    n = 8
    best = Random_solution(n)
    best_cost = Fitnes(best)
    counter = 0
    start_time = time.time()
    plot = []
    plt.ion()

    while best_cost != 0:
        T = 1.0
        Tmin = 0.001
        alpha = 0.9
        while T > Tmin:
            i = 1
            if best_cost != 0 and T > Tmin:
                print("T = " + str(T) + " best score: " + str(best_cost))
            while i < 100:
                next_solution = Mutate(best)
                next_cost = Fitnes(next_solution)
                P = np.exp(-(next_cost - best_cost) / T)
                if P > random.random():
                    best = next_solution
                    best_cost = next_cost

                    plot.append(best_cost)

                if best_cost == 0:
                    break
                i += 1
                counter += 1
            T = T * alpha

            plt.clf()
            plt.plot(plot)
            plt.draw()
            plt.pause(0.0001)

    print(best)

    print("{:g} s".format(time.time() - start_time))

    plt.ioff()
    plt.show()

    FPS = 100

    WIN_WIDTH_MIN = 10

    WIN_WIDTH = 500
    WIN_HEIGHT = 500

    if (WIN_WIDTH / n) < WIN_WIDTH_MIN:
        WIN_WIDTH = WIN_WIDTH_MIN * n
        WIN_HEIGHT = WIN_WIDTH_MIN * n

    WHITE = (255, 255, 255)
    LINE = (0, 0, 0)

    pygame.init()

    clock = pygame.time.Clock()

    logo = pygame.image.load("icon2.png")
    pygame.display.set_icon(logo)

    sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    pygame.display.set_caption("bord")
    sz_player = int(WIN_WIDTH / n)

    # порядок прорисовки важен!

    print(sz_player)
    colour = []

    for i in range(255):
        colour.append((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))

    sc.fill(WHITE)
    render = True
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    render = False
                    pos = pygame.mouse.get_pos()
                    xd = pos[0]
                    yd = pos[1]
                    color = colour[random.randint(0, n)]
                    pygame.draw.line(sc, color, (xd, yd), (xd - sz_player * xd/sz_player+1, yd - sz_player * xd/sz_player+1), 3)
                    pygame.draw.line(sc, color, (xd, yd), (xd + sz_player * (WIN_WIDTH - xd)/sz_player+1, yd - sz_player * (WIN_WIDTH - xd)/sz_player+1), 3)
                    pygame.draw.line(sc, color, (xd, yd), (xd + sz_player * (WIN_WIDTH - xd)/sz_player+1, yd + sz_player * (WIN_WIDTH - xd)/sz_player+1), 3)
                    pygame.draw.line(sc, color, (xd, yd), (xd - sz_player * xd/sz_player+1, yd + sz_player * xd/sz_player+1), 3)
                    pygame.display.update()
                if i.button == 3:
                    render = True

        sc.blit(draw(WIN_WIDTH, WIN_HEIGHT, best, sz_player), (0, 0))
        if render == True:
            pygame.display.update()
        clock.tick(FPS)