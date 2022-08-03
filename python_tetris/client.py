""" client """

from typing import Any

import pygame

from .network import Network

pygame.init()

WIDTH = 700
HEIGHT = 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


def draw(hero: Any, villain: Any) -> None:
    WIN.fill((0, 0, 0))
    hero.draw(WIN)
    villain.draw(WIN)
    pygame.display.update()


def run(n: Any, hero: Any) -> bool:
    hero.count += 1
    hero.down = hero.count == hero.velocity

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            hero.move()

    hero.move_down()
    villain = n.send(hero)

    if hero.valid() is False:
        return False

    draw(hero, villain)

    return True


def main() -> None:
    n = Network()
    hero = n.get_p()

    clock = pygame.time.Clock()

    while run(n, hero):
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
