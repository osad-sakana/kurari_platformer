import pygame
import settings


class Terrain():
    def __init__(self, surface):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, settings.GRID_SIZE, settings.GRID_SIZE)
