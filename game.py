import pygame
import settings
from stage import Stage
from title_screen import TitleScreen


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)
        self.stage_state_number = 0
        self.stage = None
        self.stage_init()
        self.is_title_screen = True
        self.title_screen = TitleScreen(self.surface)

    def stage_init(self):
        self.stage = Stage(
            self.surface, settings.STAGE_FILE_NAMES[self.stage_state_number])

    def __del__(self):
        pygame.quit()

    def run(self):
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.is_title_screen:
                        self.is_title_screen = False

            self.surface.fill(settings.COLORS["black"])

            if self.is_title_screen:
                self.title_screen.draw()
            else:
                self.stage.update()
                self.stage.draw()
                self.check_stage_clear()

            pygame.display.update()

    def check_stage_clear(self):
        if self.stage.is_clear:
            self.stage_state_number += 1
            if self.stage_state_number >= len(settings.STAGE_FILE_NAMES):
                # ゲームが終了したとき
                self.stage_state_number = 0
            self.stage_init()
