from typing import Any

import pygame

from .network import Network

pygame.init()

WIDTH = 700
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


def draw(p1: Any, p2: Any) -> None:
    WIN.fill((0, 0, 0))
    p1.draw(WIN)
    p2.draw(WIN)
    pygame.display.update()


def main() -> None:
    n = Network()
    p1 = n.get_p()

    velocity = 30

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        if p1 is None or p1.valid() is None:
            break
        p1.count += 1
        p1.down = p1.count == velocity

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                p1.move()

        p1.move_down()
        p2 = n.send(p1)
        draw(p1, p2)

    pygame.quit()


if __name__ == "__main__":
    main()
