import pygame

from .network import Network

pygame.init()

WIDTH = 700
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


def draw(p1, p2):
    WIN.fill((0, 0, 0))
    p1.draw(WIN)
    p2.draw(WIN)
    pygame.display.update()


def main():
    n = Network()
    p1 = n.get_p()

    velocity = 30

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        if not p1.valid():
            run = False
        p1.count += 1
        p1.down = p1.count == velocity

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                p1.move()

        p1.move_down()
        p2 = n.send(p1)
        draw(p1, p2)

    pygame.quit()


main()
