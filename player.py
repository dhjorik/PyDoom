import math
import pygame as pg
from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        # self.x += dx
        # self.y += dy
        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTAT * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTAT * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        player_scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * player_scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * player_scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * MAP_stepX, self.y * MAP_stepY),
                     (self.x * MAP_stepX + WIDTH * math.cos(self.angle),
                      self.y * MAP_stepY + WIDTH * math.sin(self.angle)), 2)

        pg.draw.circle(self.game.screen, 'blue', (int(self.x) * MAP_stepX, int(self.y) * MAP_stepY), 5)
        pg.draw.circle(self.game.screen, 'blue', (int(self.x + 1) * MAP_stepX, int(self.y) * MAP_stepY), 5)
        pg.draw.circle(self.game.screen, 'blue', (int(self.x) * MAP_stepX, int(self.y + 1) * MAP_stepY), 5)
        pg.draw.circle(self.game.screen, 'blue', (int(self.x + 1) * MAP_stepX, int(self.y + 1) * MAP_stepY), 5)
        pg.draw.circle(self.game.screen, 'green', (self.x * MAP_stepX, self.y * MAP_stepY), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.move()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
