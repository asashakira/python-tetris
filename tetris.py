import pygame
import tetromino
import colors
import random

UNIT = 30

FIELD_HEIGHT = 20
FIELD_WIDTH = 10

HOLD_SIZE = 4
NEXT_SIZE = 4

SPAWN = 3, 19

minos = tetromino.minos()

class Block:
    def __init__(self, playfield_x, playfield_y, color):
        self.color = color
        self.playfield_x = playfield_x
        self.playfield_y = playfield_y

    def draw(self, win, x, y):
        x = x*UNIT + self.playfield_x
        y = y*UNIT + self.playfield_y
        pygame.draw.rect(win, colors.white(), (x, y, UNIT, UNIT))
        pygame.draw.rect(win, self.color, (x+1, y+1, UNIT-2, UNIT-2))

class Tetris:
    def __init__(self, gamefield_x, gamefield_y):
        self.x, self.y = SPAWN
        self.rot = 0
        self.now = 0
        self.next = 0
        self.down = True
        self.count = 0

        self.field = [[-1 for j in range(FIELD_WIDTH)] for i in range(2*FIELD_HEIGHT)]

        # self.holdfield_x = gamefield_x
        # self.holdfield_y = gamefield_y + UNIT
        # self.playfield_x = gamefield_x + HOLD_SIZE*UNIT + UNIT
        self.playfield_x = gamefield_x + UNIT
        self.playfield_y = gamefield_y
        self.nextfield_x = self.playfield_x + FIELD_WIDTH*UNIT + UNIT
        self.nextfield_y = gamefield_y + UNIT

    def valid(self, drot=0, dx=0, dy=0): # collision detection
        x = self.x + dx
        y = self.y + dy
        rot = (self.rot + drot + 4) % 4
        for i in range(4):
            for j in range(4):
                if minos[self.now][rot][i][j] != 'x': continue
                if y+i < 0 or y+i >= 40 or x+j < 0 or x+j >= 10: return False
                if self.field[y+i][x+j] != -1: return False
        return True

    def move(self):
        keys = pygame.key.get_pressed()
        if not self.valid(self.rot, self.x, self.y+1): count = 0
        for i in range(4):
            for j in range(4):
                if minos[self.now][self.rot][i][j] == 'x':
                    self.field[self.y+i][self.x+j] = -1

        if keys[pygame.K_LEFT] and self.valid(dx=-1):
            self.x -= 1
        if keys[pygame.K_RIGHT] and self.valid(dx=1):
            self.x += 1
        if keys[pygame.K_DOWN] and self.valid(dy=1):
            self.y += 1
        if keys[pygame.K_SPACE]:
            while self.valid(dy=1):
                self.y += 1
                self.down = True
        if keys[pygame.K_x]:
            next_rot = (self.rot+1) % 4
            if self.valid(drot=1):
                self.rot = next_rot
            elif self.now != 0:
                if self.valid(drot=1, dx=1):
                    self.rot = next_rot
                    self.x += 1
                elif self.valid(drot=1, dx=1):
                    self.rot = next_rot
                    self.x -= 1
        if keys[pygame.K_z]:
            next_rot = (self.rot-1+4) % 4
            if self.valid(drot=-1):
                self.rot = next_rot
            elif self.now != 0:
                if self.valid(drot=-1, dx=1):
                    self.rot = next_rot
                    self.x += 1
                elif self.valid(drot=-1, dx=-1):
                    self.rot = next_rot
                    self.x -= 1

    def move_down(self):
        erase = []
        if self.down:
            self.count = 0
            if self.valid(dy=1):
                self.y += 1
            else:
                for dy in range(4):
                    for dx in range(4):
                        if minos[self.now][self.rot][dy][dx] == 'x':
                            self.field[self.y+dy][self.x+dx] = self.now

                for dy in range(4):
                    line = True
                    if self.y+dy < 0 or self.y+dy >= 40: continue
                    for nx in range(10):
                        if self.field[self.y+dy][nx] == -1:
                            line = False
                    if line: erase.append(self.y+dy)

                self.now = (self.now + 1) % 7
                # self.next = (self.now+1)%7
                self.x, self.y = SPAWN
                self.rot = 0

        for e in erase:
            for nx in range(10):
                for ny in range(e, 0, -1):
                   self.field[ny][nx] = self.field[ny-1][nx]
                self.field[0][nx] = -1

    def draw(self, win):
        self.draw_grid(win)
        self.draw_field(win)
        self.draw_mino(win)
        # self.draw_hold(win)
        # self.draw_next(win)

    def draw_field(self, win):
        colors = tetromino.colors()
        for y in range(FIELD_HEIGHT, 2*FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.field[y][x] == -1: continue;
                block = Block(self.playfield_x, self.playfield_y, colors[self.field[y][x]])
                block.draw(win, x, y-FIELD_HEIGHT)

    def draw_mino(self, win):
        colors = tetromino.colors()
        for i in range(4):
            for j in range(4):
                if minos[self.now][self.rot][i][j] != 'x': continue
                block = Block(self.playfield_x, self.playfield_y, colors[self.now])
                block.draw(win, self.x+j, self.y+i-FIELD_HEIGHT)

    def draw_hold(self, win):
        for i in range(HOLD_SIZE + 1):
            color = colors.gray()
            start = self.holdfield_x, UNIT*i + self.holdfield_y
            end = UNIT*HOLD_SIZE + self.holdfield_x, UNIT*i + self.holdfield_y
            if i == 0 or i == HOLD_SIZE: color = colors.white()
            pygame.draw.line(win, color, start, end)

        for i in range(HOLD_SIZE + 1):
            color = colors.gray()
            start = self.holdfield_x + UNIT*i, self.holdfield_y
            end = UNIT*i + self.holdfield_x, UNIT*HOLD_SIZE + self.holdfield_y
            if i == 0 or i == HOLD_SIZE: color = colors.white()
            pygame.draw.line(win, color, start, end)

    def draw_grid(self, win):
        for i in range(FIELD_HEIGHT + 1):
            color = colors.gray()
            start = self.playfield_x, UNIT*i + self.playfield_y
            end = UNIT*FIELD_WIDTH + self.playfield_x, UNIT*i + self.playfield_y
            if i == FIELD_HEIGHT: color = colors.white()
            pygame.draw.line(win, color, start, end)

        for i in range(FIELD_WIDTH + 1):
            color = colors.gray()
            start = self.playfield_x + UNIT*i, self.playfield_y
            end = UNIT*i + self.playfield_x, UNIT*FIELD_HEIGHT + self.playfield_y
            if i == 0 or i == FIELD_WIDTH: color = colors.white()
            pygame.draw.line(win, color, start, end)

    def draw_next(self, win):
        for i in range(NEXT_SIZE + 1):
            color = colors.gray()
            start = self.nextfield_x, UNIT*i + self.nextfield_y
            end = UNIT*NEXT_SIZE + self.nextfield_x, UNIT*i + self.nextfield_y
            if i == 0 or i == NEXT_SIZE: color = colors.white()
            pygame.draw.line(win, color, start, end)

        for i in range(NEXT_SIZE + 1):
            color = colors.gray()
            start = self.nextfield_x + UNIT*i, self.nextfield_y
            end = UNIT*i + self.nextfield_x, UNIT*NEXT_SIZE + self.nextfield_y
            if i == 0 or i == NEXT_SIZE: color = colors.white()
            pygame.draw.line(win, color, start, end)

