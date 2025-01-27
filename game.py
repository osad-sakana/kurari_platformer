import pygame
import settings
from stage import Stage


class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)
        self.stage = Stage(self.surface)

    def __del__(self):
        pygame.quit()

    def run(self):
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.surface.fill(settings.COLORS["black"])

            self.stage.update()
            self.stage.draw()

            pygame.display.update()
