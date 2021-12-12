import pygame
import random
import tetromino
import colors

pygame.init()
WIN_WIDTH = 800
WIN_HEIGHT = 1000
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tetris")

BLOCK = 30

XBUF = WIN_WIDTH//2 - 150
YBUF = 200

class Block:
    def __init__(self, color):
        self.color = color
        self.width = BLOCK
        self.height = BLOCK

    def draw(self, x, y):
        x *= self.width
        y *= self.height
        x += XBUF
        y += YBUF
        pygame.draw.rect(WIN, colors.white(), (x, y, self.width, self.height))
        pygame.draw.rect(WIN, self.color, (x+1, y+1, self.width-2, self.height-2))

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def draw(self, x, y, r):
        block = Block(self.color)
        shape = self.shape[r]
        for i in range(4):
            for j in range(4):
                if shape[i][j] == '.': continue
                block.draw(x+j, y+i)

def draw_grid():
    for i in range(21):
        color = colors.gray()
        start_pos = XBUF, BLOCK*i + YBUF
        end_pos = BLOCK*10 + XBUF, BLOCK*i + YBUF
        if i == 20: color = colors.white()
        pygame.draw.line(WIN, color, start_pos, end_pos)
    for i in range(11):
        color = colors.gray()
        start_pos = BLOCK*i + XBUF, YBUF
        end_pos = BLOCK*i + XBUF, BLOCK*20 + YBUF
        if i == 0 or i == 10: color = colors.white()
        pygame.draw.line(WIN, color, start_pos, end_pos)

def draw_field(field):
    colors = tetromino.colors()
    for y in range(20):
        for x in range(10):
            if field[y][x] == -1: continue;
            block = Block(colors[field[y][x]])
            block.draw(x, y)

def draw(field):
    WIN.fill(colors.black())

    draw_grid()
    #draw_field(field)

    pygame.display.update()

def main():
    tetro = tetromino.tetromino()

    # play field
    field = [[-1 for j in range(10)] for i in range(20)]

    now = 0      # tetromino piece
    rotation = 0 # mod 4
    x, y = 3, 0  # current piece's x, y

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i in range(4):
            for j in range(4):
                if tetro[now][rotation][i][j] == 'x':
                    field[y+i][x+j] = now

        draw(field)

    pygame.quit()


if __name__ == '__main__':
    main()

