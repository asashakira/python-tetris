""" main2 """

from __future__ import annotations

import pygame

from .tetris import Tetris

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 1000

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tetris")


def draw(tetris) -> None:
    WIN.fill((0, 0, 0))
    tetris.draw(WIN)
    pygame.display.update()


def run(tetris) -> bool:
    tetris.count += 1
    tetris.down = tetris.count == tetris.velocity
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tetris.run = False

        if event.type == pygame.KEYDOWN:
            tetris.move()

    # move tetris piece down
    tetris.move_down()

    if tetris.valid() is False:
        return False

    if tetris.run is False:
        return False

    # draw to window
    draw(tetris)

    return True


def main() -> None:
    tetris = Tetris(200, 200, velocity=30)
    clock = pygame.time.Clock()

    while run(tetris):
        clock.tick(60)

    print("GAME OVER")
    pygame.quit()


if __name__ == "__main__":
    print("###########")
    print("#         #")
    print("####   ####")
    print("   #   #   ")
    print("   #####   ")
    main()
