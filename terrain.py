import pygame
import settings

terrain_colors = {
    0: settings.COLORS["black"],
    1: settings.COLORS["green"],
    2: settings.COLORS["blue"],
    3: settings.COLORS["red"],
    4: settings.COLORS["white"],
}


class Terrain():
    def __init__(self, surface, grid_x, grid_y, terrain_color):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, settings.GRID_SIZE, settings.GRID_SIZE)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect.x = grid_x * settings.GRID_SIZE
        self.rect.y = grid_y * settings.GRID_SIZE
        self.color = terrain_colors[terrain_color]
        self.damage = self.set_terrain_damage(terrain_color)
        self.is_goal = self.set_terrain_goal(terrain_color)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def set_terrain_damage(self, terrain_color):
        if terrain_color == 3:
            return 1
        return 0

    def set_terrain_goal(self, terrain_color):
        if terrain_color == 2:
            return True
        return False
