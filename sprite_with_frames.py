import pygame


class SpriteWithFrames(pygame.sprite.Sprite):
    def __init__(self, surface, pos, image_url, image_cols, image_rows, sprite_width, sprite_height, image_is_reverse=False):
        super().__init__()
        self.surface = surface
        self.frames = self._load_sprite_sheet(image_url, image_cols, image_rows)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = pygame.Rect(pos[0], pos[1], sprite_width, sprite_height)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        self.frame_current_row = 0
        self.image_cols = image_cols
        self.image_rows = image_rows
        self.image_is_reverse = image_is_reverse

    @staticmethod
    def _load_sprite_sheet(filename, cols, rows):
        sheet = pygame.image.load(filename).convert_alpha()
        sprite_width = sheet.get_width() // cols
        sprite_height = sheet.get_height() // rows
        sprites = []
        for i in range(rows):
            for j in range(cols):
                rect = pygame.Rect(j * sprite_width, i * sprite_height, sprite_width, sprite_height)
                frame = sheet.subsurface(rect)
                sprites.append(frame)
        return sprites

    def _frame_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % self.image_cols
            self.frame_index += self.frame_current_row * self.image_cols
            self.image = self.frames[self.frame_index]

    def draw(self, magnification_rate=1):
        draw_rect = self.image.get_rect(center=self.rect.center)
        if magnification_rate != 1:
            scaled_image = pygame.transform.scale(self.image, (int(self.rect.width * magnification_rate), int(self.rect.height * magnification_rate)))
            draw_rect = scaled_image.get_rect(center=self.rect.center)
        else:
            scaled_image = self.image

        if self.image_is_reverse:
            flipped_image = pygame.transform.flip(scaled_image, True, False)
            self.surface.blit(flipped_image, draw_rect)
        else:
            self.surface.blit(scaled_image, draw_rect)
