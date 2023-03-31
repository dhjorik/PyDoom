import pygame as pg
import sys
import math
import logging

from settings import *
from map import *
from player import *
from raycasting import *
from objects import *

class DoomGame:
    def __init__(self):
        ppass, pfail = pg.init()
        self.screen = pg.display.set_mode(RES)
        pg.mouse.set_visible(False)

        self.clock = pg.time.Clock()
        self.frame = pg.time.Clock()

        self.delta_time = 1
        self.delta_frame = 1

        self.fps = 0
        self.fps_max = 0
        self.fps_min = 10000

        self.refresh_delay = 0
        self.map = None
        self.player = None
        self.raycast = None
        self.object_renderer = None
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycast = RayCasting(self)

    def update(self):
        self.player.update()
        self.raycast.update()
        pg.display.flip()
        self.refresh_delay += 1
        self.delta_time = self.clock.tick(TICK)
        sin_a = math.sin(self.player.angle)
        cos_a = math.cos(self.player.angle)

        self.fps = self.clock.get_fps()
        if self.fps>self.fps_max: self.fps_max = self.fps
        if self.fps<self.fps_min: self.fps_min = self.fps

        msg1 = f'{self.fps_min:.1f}<{self.fps:.1f}<{self.fps_max:.1f} {self.delta_time:.1f}'
        msg2 = f'{self.frame.get_fps():.1f} {self.delta_frame:.1f}'
        msg3 = f'{self.player.pos} {self.player.map_pos} {self.player.angle:.2f} {sin_a:.2f} {cos_a:.2f}'
        pg.display.set_caption(f'{msg1} --- {msg2} --- {msg3}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        # self.map.draw()
        # self.player.draw()
        self.delta_frame = self.frame.tick()

    def check_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            if self.refresh_delay > REFRESH:
                self.refresh_delay = 0
                self.fps_min = self.fps
                self.fps_max = self.fps


if __name__ == '__main__':
    log.info('Starting pyDOOM')
    game = DoomGame()
    game.run()
