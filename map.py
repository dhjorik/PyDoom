import pygame as pg
from settings import *


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map.copy()
        self.world_map = {}
        self.rows = MAP_rows
        self.cols = MAP_cols

        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * MAP_stepX, pos[1] * MAP_stepY, MAP_stepX, MAP_stepY), 2)
         for pos in self.world_map]
