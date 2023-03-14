import math
import pygame as pg
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + TOL
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontals
            y_horz, hdy = (y_map + 1, 1) if sin_a > 0 else (y_map - TOL, -1)
            depth_horz = (y_horz - oy) / sin_a
            x_horz = ox + depth_horz * cos_a
            depth_deltah = hdy / sin_a
            hdx = depth_deltah * cos_a

            for i in range(MAX_DEPTH):
                search_tile = int(x_horz), int(y_horz)
                if search_tile in self.game.map.world_map:
                    # Tile found, break loop
                    break
                x_horz += hdx
                y_horz += hdy
                depth_horz += depth_deltah

            # verticals
            x_vert, vdx = (x_map + 1, 1) if cos_a > 0 else (x_map - TOL, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            depth_deltav = vdx / cos_a
            vdy = depth_deltav * sin_a

            for i in range(MAX_DEPTH):
                search_tile = int(x_vert), int(y_vert)
                if search_tile in self.game.map.world_map:
                    # Tile found, break loop
                    break
                x_vert += vdx
                y_vert += vdy
                depth_vert += depth_deltav

            if depth_vert < depth_horz:
                depth = depth_vert
            else:
                depth = depth_horz

            pg.draw.line(self.game.screen, 'lightgreen',
                         (MAP_stepX * ox, MAP_stepY * oy),
                         (MAP_stepX * ox + MAP_stepX * depth * cos_a, MAP_stepY * oy + MAP_stepY * depth * sin_a),
                         2)
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
