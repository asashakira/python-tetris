import pygame
import random
import tetris

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 1000
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tetris")

class Block:
    def __init__(self, color, width=20, height=20):
        self.color = color
        self.width = width
        self.height = height

    def draw(self, x, y):
        pygame.draw.rect(WIN, (255, 255, 255), (x, y, self.width, self.height))
        pygame.draw.rect(WIN, self.color, (x+1, y+1, self.width-2, self.height-2))

class Tetromino:
    def __init__(self):
        self.shape = tetris.shapes()[0][0]
        self.color = tetris.colors()[random.randint(0, 6)]

    def draw(self, x, y):
        block = Block(self.color)
        for i in range(5):
            for j in range(5):
                if self.shape[i][j] == '.': continue
                block.draw(x + block.width*j, y + block.height*i)

def main():
    tet = Tetromino()
    tet2 = Tetromino()
    x, y = 100, 0
    v = 20
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #y = 0 if y+v == WIN_HEIGHT else y+v
        x = 0 if x+v == WIN_WIDTH else x+v

        WIN.fill((0,0,0))
        tet.draw(x, y)
        tet2.draw(x, y+100)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()

