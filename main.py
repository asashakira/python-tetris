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

FIELD_HEIGHT = 20
FIELD_WIDTH = 10

SPAWN = 3, 19

# play field
field = [[-1 for j in range(10)] for i in range(40)]

# mino shapes and colors
minos = tetromino.minos()

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

def draw_grid():
    for i in range(FIELD_HEIGHT+1):
        color = colors.gray()
        start_pos = XBUF, BLOCK*i + YBUF
        end_pos = BLOCK*FIELD_WIDTH + XBUF, BLOCK*i + YBUF
        if i == FIELD_HEIGHT: color = colors.white()
        pygame.draw.line(WIN, color, start_pos, end_pos)

    for i in range(FIELD_WIDTH+1):
        color = colors.gray()
        start_pos = BLOCK*i + XBUF, YBUF
        end_pos = BLOCK*i + XBUF, BLOCK*FIELD_HEIGHT + YBUF
        if i == 0 or i == FIELD_WIDTH: color = colors.white()
        pygame.draw.line(WIN, color, start_pos, end_pos)

def draw_field():
    colors = tetromino.colors()
    for y in range(FIELD_HEIGHT, 2*FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            if field[y][x] == -1: continue;
            block = Block(colors[field[y][x]])
            block.draw(x, y-FIELD_HEIGHT)

def draw_mino(now, rot, x, y):
    colors = tetromino.colors()
    for i in range(4):
        for j in range(4):
            if minos[now][rot][i][j] != 'x': continue
            block = Block(colors[now])
            block.draw(x+j, y+i-FIELD_HEIGHT)

def draw_next_mino(nxt):
    tetromino.colors()
    block = Block(colors[nxt])
    block.draw(0-2, 0)

def valid(now, rot, x, y): # collision detection
    for i in range(4):
        for j in range(4):
            if minos[now][rot][i][j] != 'x': continue
            if y+i < 0 or y+i >= 40 or x+j < 0 or x+j >= 10: return False
            if field[y+i][x+j] != -1: return False
    return True

def main():
    now = random.randrange(7)
    nxt = random.randrange(7)
    rot = 0
    x, y = SPAWN

    count = 0
    velocity = 10
    down = False

    run = True
    while run:
        if not valid(now, rot, x, y): run = False
        pygame.time.delay(30)
        count += 1
        down = count == velocity
        erase = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if not valid(now, rot, x, y+1): count = 0
                for i in range(4):
                    for j in range(4):
                        if minos[now][rot][i][j] == 'x':
                            field[y+i][x+j] = -1

                if event.key == pygame.K_LEFT and valid(now, rot, x-1, y):
                    x -= 1
                if event.key == pygame.K_RIGHT and valid(now, rot, x+1, y):
                    x += 1
                if event.key == pygame.K_DOWN and valid(now, rot, x, y+1):
                    y += 1
                if event.key == pygame.K_SPACE:
                    while valid(now, rot, x, y+1):
                        y += 1
                        down = True
                if event.key == pygame.K_x:
                    next_rot = (rot+1) % 4
                    if valid(now, next_rot, x, y):
                        rot = next_rot
                    elif now == 0:
                        continue
                    elif valid(now, next_rot, x+1, y):
                        rot = next_rot
                        x += 1
                    elif valid(now, next_rot, x-1, y):
                        rot = next_rot
                        x -= 1
                if event.key == pygame.K_z:
                    next_rot = (rot-1+4) % 4
                    if valid(now, next_rot, x, y):
                        rot = next_rot
                    elif now == 0:
                        continue
                    elif valid(now, next_rot, x+1, y):
                        rot = next_rot
                        x += 1
                    elif valid(now, next_rot, x-1, y):
                        rot = next_rot
                        x -= 1

        if down:
            count = 0
            if valid(now, rot, x, y+1):
                y += 1
            else:
                for dy in range(4):
                    for dx in range(4):
                        if minos[now][rot][dy][dx] == 'x':
                            field[y+dy][x+dx] = now

                for dy in range(4):
                    line = True
                    if y+dy < 0 or y+dy >= 40: continue
                    for nx in range(10):
                        if field[y+dy][nx] == -1:
                            line = False
                    if line: erase.append(y+dy)

                now = nxt
                nxt = random.randrange(7)
                x, y = SPAWN
                rot = 0

        for e in erase:
            for nx in range(10):
                for ny in range(e, 0, -1):
                   field[ny][nx] = field[ny-1][nx]
                field[0][nx] = -1

        WIN.fill(colors.black())
        draw_grid()
        draw_field()
        draw_mino(now, rot, x, y)
        pygame.display.update()

    print("GAME OVER")
    pygame.quit()

if __name__ == '__main__':
    print("###########")
    print("#         #")
    print("####   ####")
    print("   #   #   ")
    print("   #####   ")
    main()

