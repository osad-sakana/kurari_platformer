import pygame
import settings


class SpriteWithFrames(pygame.sprite.Sprite):
    def __init__(self, surface, pos, image_url, image_cols, image_rows, sprite_width, sprite_height, image_is_reverse=False):
        super().__init__()
        self.surface = surface
        self.frames = self._load_sprite_sheet(
            image_url, image_cols, image_rows)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
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
                rect = pygame.Rect(j * sprite_width, i *
                                   sprite_height, sprite_width, sprite_height)
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

    def draw(
        self,
        magnification_rate=1,
        is_center=True,
        is_player=False,
    ):
        """
        スプライトを描画する。
        """
        # ステップ1: 画像を必要に応じて反転（拡大縮小前に実行）
        current_image = self.image
        if self.image_is_reverse:
            current_image = pygame.transform.flip(current_image, True, False)

        # ステップ2: 画像を拡大縮小（プレイヤーの場合は特別処理）
        if is_player:
            player_width = settings.GRID_SIZE * 3
            scaled_height = int(self.rect.height * magnification_rate)
            draw_image = pygame.transform.scale(
                current_image, (player_width, scaled_height))
        else:
            scaled_width = int(self.rect.width * magnification_rate)
            scaled_height = int(self.rect.height * magnification_rate)
            draw_image = pygame.transform.scale(
                current_image, (scaled_width, scaled_height))

        # ステップ3: 描画位置の設定（画像サイズから新しいRectを作成）
        draw_rect = draw_image.get_rect()

        if is_center:
            draw_rect.center = self.rect.center
        else:
            draw_rect.topleft = self.rect.topleft

        # ステップ4: 描画を実行
        self.surface.blit(draw_image, draw_rect)

        # ステップ5: デバッグモード時の表示
        if settings.IS_DEBUG_MODE:
            pygame.draw.rect(
                self.surface, settings.COLORS["red"], draw_rect, 2)
            pygame.draw.rect(
                self.surface, settings.COLORS["blue"], self.rect, 2)
