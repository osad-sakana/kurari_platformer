import pygame
import settings


class Player():
    def __init__(self, surface):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, settings.GRID_SIZE, settings.GRID_SIZE)
        self.dx = 0  # x方向の速度
        self.dy = 0  # y方向の速度

    def update(self):
        # キー入力を受け付けて移動する
        self.key_control()

    def draw(self):
        pygame.draw.rect(self.surface, settings.COLORS["white"], self.rect)

    def move_left_right(self, dx):
        self.rect.x += dx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH

    def key_control(self):
        key = pygame.key.get_pressed()

        # 左右の移動に関するキーコントロール
        if key[pygame.K_LEFT]:
            self.dx -= settings.PLAYER_ACCELERATION
            if self.dx < -settings.PLAYER_MAX_SPEED:
                self.dx = -settings.PLAYER_MAX_SPEED
        if key[pygame.K_RIGHT]:
            self.dx += settings.PLAYER_ACCELERATION
            if self.dx > settings.PLAYER_MAX_SPEED:
                self.dx = settings.PLAYER_MAX_SPEED
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            if self.dx > 0:
                self.dx -= settings.PLAYER_ACCELERATION
                if self.dx < 0:
                    self.dx = 0
            if self.dx < 0:
                self.dx += settings.PLAYER_ACCELERATION
                if self.dx > 0:
                    self.dx = 0

        self.move_left_right(self.dx)
