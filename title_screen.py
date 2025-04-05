import pygame
import settings
import time
from math import sin


class TitleScreen:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font("PixelMplus12-Regular.ttf", 32)
        self.start_time = time.time()

    def draw(self):
        title_text = self.font.render(
            settings.TITLE, True, settings.COLORS["white"])
        start_text = self.font.render(
            "Press Space Key", True, settings.COLORS["white"])

        title_rect = title_text.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 50)
        )
        start_rect = start_text.get_rect(
            center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 50)
        )

        self.surface.blit(title_text, title_rect)

        # 点滅効果の計算
        elapsed_time = time.time() - self.start_time
        alpha = int((1 + sin(elapsed_time * 3)) * 127 + 128)  # 0-255の範囲で点滅
        start_text.set_alpha(alpha)
        self.surface.blit(start_text, start_rect)
