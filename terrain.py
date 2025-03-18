# import pygame
import settings
from sprite_with_frames import SpriteWithFrames

terrain_colors = {
    0: settings.COLORS["black"],
    1: settings.COLORS["green"],
    2: settings.COLORS["blue"],
    3: settings.COLORS["red"],
    4: settings.COLORS["white"],
}

terrain_indexes = {
    0: 5,
    1: 6,
    2: 7,
    3: 8,
    4: 34,
    5: 122,
    6: 94,
    7: 95,
    8: 96,
    9: 215,
}

TERRAIN_IMAGE_URL = "./assets/images/terrain.png"
TERRAIN_IMAGE_SIZE = 16
TERRAIN_WIDTH = 22
TERRAIN_HEIGHT = 11


class Terrain(SpriteWithFrames):
    def __init__(self, surface, grid_x, grid_y, terrain_color):
        super().__init__(
            surface=surface,
            pos=(grid_x * settings.GRID_SIZE, grid_y * settings.GRID_SIZE),
            image_url=TERRAIN_IMAGE_URL,
            image_cols=TERRAIN_WIDTH,
            image_rows=TERRAIN_HEIGHT,
            sprite_width=TERRAIN_IMAGE_SIZE,
            sprite_height=TERRAIN_IMAGE_SIZE,
            image_is_reverse=False,
        )
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * settings.GRID_SIZE
        self.rect.y = grid_y * settings.GRID_SIZE
        # rectを2倍のサイズにする
        self.rect.width = settings.GRID_SIZE
        self.rect.height = settings.GRID_SIZE
        self.color = terrain_indexes[terrain_color]
        self.image = self.frames[self.color]
        self.damage = self.set_terrain_damage(terrain_color)
        self.is_goal = self.set_terrain_goal(terrain_color)

    def draw(self):
        super().draw(
            magnification_rate=1,
            is_center=False,
        )

    def set_terrain_damage(self, terrain_color):
        if terrain_color in [6, 7, 8]:
            return 1
        return 0

    def set_terrain_goal(self, terrain_color):
        if terrain_color == 9:
            return True
        return False
