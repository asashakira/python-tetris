""" all the Tets"""

from __future__ import annotations

import pygame

from .colors import COLORS, GRAY, WHITE
from .tetromino import get_minos

UNIT = 30

FIELD_HEIGHT = 20
FIELD_WIDTH = 10

HOLD_SIZE = 4
NEXT_SIZE = 4

SPAWN = 3, 19

MINOS = get_minos()


class Block:
    """Block class that represents a single 'block'"""

    def __init__(
        self, playfield_x: int, playfield_y: int, color: tuple[int, int, int]
    ) -> None:
        self.color = color
        self.playfield_x = playfield_x
        self.playfield_y = playfield_y

    def draw(self, win: pygame.Surface, x: int, y: int) -> None:
        x = x * UNIT + self.playfield_x
        y = y * UNIT + self.playfield_y
        pygame.draw.rect(win, WHITE, (x, y, UNIT, UNIT))
        pygame.draw.rect(win, self.color, (x + 1, y + 1, UNIT - 2, UNIT - 2))


class Tetris:
    """Tetris class"""

    def __init__(self, gamefield_x: int, gamefield_y: int, velocity=30) -> None:
        # position
        self.x, self.y = SPAWN

        # rotation
        self.rot = 0

        # piece
        self.now = 0
        self.next = 0

        # control fall
        self.down = True
        self.count = 0
        self.velocity = velocity

        # play field data
        self.field = [[-1 for _ in range(FIELD_WIDTH)] for _ in range(2 * FIELD_HEIGHT)]
        self.erase = []

        # game running
        self.run = True

        # play field ui
        self.holdfield_x = gamefield_x
        self.holdfield_y = gamefield_y + UNIT
        self.playfield_x = gamefield_x + HOLD_SIZE * UNIT + UNIT
        self.playfield_x = gamefield_x + UNIT
        self.playfield_y = gamefield_y
        self.nextfield_x = self.playfield_x + FIELD_WIDTH * UNIT + UNIT
        self.nextfield_y = gamefield_y + UNIT

    # collision detection
    def valid(self, drot: int = 0, dx: int = 0, dy: int = 0) -> bool:
        x = self.x + dx
        y = self.y + dy
        rot = (self.rot + drot + 4) % 4
        for i in range(4):
            for j in range(4):
                if MINOS[self.now][rot][i][j] != "x":
                    continue
                if y + i < 0 or y + i >= 40 or x + j < 0 or x + j >= 10:
                    return False
                if self.field[y + i][x + j] != -1:
                    return False
        return True

    def move(self) -> None:
        keys = pygame.key.get_pressed()

        # move left or right
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()

        # soft drop
        if keys[pygame.K_DOWN]:
            self.soft_drop()

        # hard drop
        if keys[pygame.K_SPACE]:
            self.hard_drop()

        # rotates clockwise
        if keys[pygame.K_x]:
            self.rotate_clockwise()

        # rotates counter clockwise
        if keys[pygame.K_z]:
            self.rotate_counter_clockwise()

        self.reset_field()

    def reset_field(self) -> None:
        for i in range(4):
            for j in range(4):
                if MINOS[self.now][self.rot][i][j] == "x":
                    self.field[self.y + i][self.x + j] = -1

    def move_left(self) -> None:
        if self.valid(dx=-1):
            self.x -= 1

    def move_right(self) -> None:
        if self.valid(dx=1):
            self.x += 1

    def soft_drop(self) -> None:
        if self.valid(dy=1):
            self.y += 1

    def hard_drop(self) -> None:
        while self.valid(dy=1):
            self.y += 1
            self.down = True

    def rotate_clockwise(self) -> None:
        """rotates counter clockwise"""
        next_rot = (self.rot + 1) % 4
        if self.valid(drot=1):
            self.rot = next_rot
        elif self.now != 0:
            if self.valid(drot=1, dx=1):
                self.rot = next_rot
                self.x += 1
            elif self.valid(drot=1, dx=1):
                self.rot = next_rot
                self.x -= 1

    def rotate_counter_clockwise(self) -> None:
        """rotates counter clockwise"""
        next_rot = (self.rot - 1 + 4) % 4
        if self.valid(drot=-1):
            self.rot = next_rot
        elif self.now != 0:
            if self.valid(drot=-1, dx=1):
                self.rot = next_rot
                self.x += 1
            elif self.valid(drot=-1, dx=-1):
                self.rot = next_rot
                self.x -= 1

    def set_mino(self) -> None:
        """set mino to field"""
        for dy in range(4):
            for dx in range(4):
                if MINOS[self.now][self.rot][dy][dx] == "x":
                    self.field[self.y + dy][self.x + dx] = self.now

    # check if row is filled
    def check_row(self, y) -> bool:
        for x in range(10):
            if self.field[y][x] == -1:
                return False
        return True

    # find filled rows
    def find_rows(self) -> None:
        """find lines to erase"""
        for dy in range(4):
            ny = self.y + dy
            if ny >= 40:
                return
            if self.check_row(ny):
                self.erase.append(ny)

    def erase_rows(self) -> None:
        """erase the lines"""
        self.find_rows()  # find lines to erase
        for e in self.erase:
            for nx in range(10):
                for ny in range(e, 0, -1):
                    self.field[ny][nx] = self.field[ny - 1][nx]
                self.field[0][nx] = -1
        self.erase = []

    def set_now_mino(self) -> None:
        self.now = (self.now + 1) % 7

    def set_next_mino(self) -> None:
        self.next = (self.now + 1) % 7

    def reset_mino(self) -> None:
        self.x, self.y = SPAWN
        self.rot = 0

    def move_down(self) -> None:
        if not self.down:
            return

        self.count = 0

        # move mino down if valid
        if self.valid(dy=1):
            self.y += 1
            return

        self.set_mino()  # lock mino into place
        self.erase_rows()  # erase rows

        self.set_now_mino()
        self.set_next_mino()

        # reset
        self.reset_mino()

    def draw(self, win: pygame.Surface) -> None:
        self.draw_grid(win)
        self.draw_field(win)
        self.draw_mino(win)
        # self.draw_hold(win)
        # self.draw_next(win)

    def draw_field(self, win: pygame.Surface) -> None:
        colors = COLORS
        for y in range(FIELD_HEIGHT, 2 * FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.field[y][x] == -1:
                    continue
                block = Block(
                    self.playfield_x, self.playfield_y, colors[self.field[y][x]]
                )
                block.draw(win, x, y - FIELD_HEIGHT)

    def draw_mino(self, win: pygame.Surface) -> None:
        colors = COLORS
        for i in range(4):
            for j in range(4):
                if MINOS[self.now][self.rot][i][j] != "x":
                    continue
                block = Block(self.playfield_x, self.playfield_y, colors[self.now])
                block.draw(win, self.x + j, self.y + i - FIELD_HEIGHT)

    def draw_hold(self, win: pygame.Surface) -> None:
        for i in range(HOLD_SIZE + 1):
            color = GRAY
            start = self.holdfield_x, UNIT * i + self.holdfield_y
            end = UNIT * HOLD_SIZE + self.holdfield_x, UNIT * i + self.holdfield_y
            if i in (0, HOLD_SIZE):
                color = WHITE
            pygame.draw.line(win, color, start, end)

        for i in range(HOLD_SIZE + 1):
            color = GRAY
            start = self.holdfield_x + UNIT * i, self.holdfield_y
            end = UNIT * i + self.holdfield_x, UNIT * HOLD_SIZE + self.holdfield_y
            if i in (0, HOLD_SIZE):
                color = WHITE
            pygame.draw.line(win, color, start, end)

    def draw_grid(self, win: pygame.Surface) -> None:
        for i in range(FIELD_HEIGHT + 1):
            color = GRAY
            start = self.playfield_x, UNIT * i + self.playfield_y
            end = UNIT * FIELD_WIDTH + self.playfield_x, UNIT * i + self.playfield_y
            if i == FIELD_HEIGHT:
                color = WHITE
            pygame.draw.line(win, color, start, end)

        for i in range(FIELD_WIDTH + 1):
            color = GRAY
            start = self.playfield_x + UNIT * i, self.playfield_y
            end = UNIT * i + self.playfield_x, UNIT * FIELD_HEIGHT + self.playfield_y
            if i in (0, FIELD_WIDTH):
                color = WHITE
            pygame.draw.line(win, color, start, end)

    def draw_next(self, win: pygame.Surface) -> None:
        for i in range(NEXT_SIZE + 1):
            color = GRAY
            start = self.nextfield_x, UNIT * i + self.nextfield_y
            end = UNIT * NEXT_SIZE + self.nextfield_x, UNIT * i + self.nextfield_y
            if i in (0, NEXT_SIZE):
                color = WHITE
            pygame.draw.line(win, color, start, end)

        for i in range(NEXT_SIZE + 1):
            color = GRAY
            start = self.nextfield_x + UNIT * i, self.nextfield_y
            end = UNIT * i + self.nextfield_x, UNIT * NEXT_SIZE + self.nextfield_y
            if i in (0, NEXT_SIZE):
                color = WHITE
            pygame.draw.line(win, color, start, end)
