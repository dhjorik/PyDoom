import math
import pygame as pg
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result.clear()
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_horz, texture_vert = 1, 1

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
                    texture_horz = self.game.map.world_map[search_tile]
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
                    texture_vert = self.game.map.world_map[search_tile]
                    break
                x_vert += vdx
                y_vert += vdy
                depth_vert += depth_deltav

            if depth_vert < depth_horz:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_horz, texture_horz
                x_horz %= 1
                offset = (1 - x_horz) if sin_a > 0 else (1 - x_horz)

            # Fishball correction
            depth_fb = depth * math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth_fb + TOL)

            # pg.draw.line(self.game.screen, 'lightgreen',
            #              (MAP_stepX * ox, MAP_stepY * oy),
            #              (MAP_stepX * ox + MAP_stepX * depth * cos_a, MAP_stepY * oy + MAP_stepY * depth * sin_a),
            #              2)

            # depth_color = [255 / (1 + depth ** 5 * TOL)] * 3
            # pg.draw.rect(self.game.screen, depth_color,
            #              (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            self.ray_casting_result.append((depth, proj_height, texture, offset))
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
