import pygame
import settings
from sprite_with_frames import SpriteWithFrames

IMAGE_URL = "./assets/images/$Gunman_1.png"
IMAGE_ROWS = 4
IMAGE_COLS = 4
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 96


class Player(SpriteWithFrames):
    def __init__(self, surface, map, pos):
        super().__init__(
            surface=surface,
            pos=pos,
            image_url=IMAGE_URL,
            image_cols=IMAGE_COLS,
            image_rows=IMAGE_ROWS,
            sprite_width=SPRITE_WIDTH,
            sprite_height=SPRITE_HEIGHT,
            image_is_reverse=True,
        )

        self.dx = 0  # x方向の速度
        self.dy = 0  # y方向の速度
        self.map = map
        self.hp = 100
        self.max_hp = 100
        self.is_clear = False

    def update(self):
        # キー入力を受け付けて移動する
        self.frame_current_row = 0
        self.key_control()
        self.move_up_down()
        self.fall()
        self.move_left_right(self.dx)

        super()._frame_animation()

    def draw(self):
        # プレイヤーの画像を中央寄せで描画する
        if settings.IS_DEBUG_MODE:
            pygame.draw.rect(self.surface, settings.COLORS["blue"], self.rect, 1)
        super().draw()

    def move_left_right(self, dx):
        self.rect.x += dx

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH

        self._collide_left_right()

    def key_control(self):
        key = pygame.key.get_pressed()

        # 左右の移動に関するキーコントロール
        if key[pygame.K_LEFT]:
            self.image_is_reverse = False
            self.frame_current_row = 2
            self.dx -= settings.PLAYER_ACCELERATION
            if self.dx < -settings.PLAYER_MAX_SPEED:
                self.dx = -settings.PLAYER_MAX_SPEED
        if key[pygame.K_RIGHT]:
            self.image_is_reverse = True
            self.frame_current_row = 2
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

        # ジャンプに関するキーコントロール
        if key[pygame.K_SPACE] and self._on_ground():
            self.dy = -settings.PLAYER_JUMP_POWER
        if not self._on_ground():
            self.frame_current_row = 1

    def move_up_down(self):
        # 重力
        self.dy += settings.PLAYER_GRAVITY

        # 最高速度を適用
        if self.dy > settings.PLAYER_MAX_SPEED:
            self.dy = settings.PLAYER_MAX_SPEED

        # 加速度を反映
        self.rect.y += self.dy

        self._collide_up_down()

    def _collide_up_down(self):
        if self.dy > 0:
            # 下方向の衝突判定
            for obj in self.map.map_objects:
                if self.rect.colliderect(obj.rect):
                    self.rect.bottom = obj.rect.top
                    self.dy = 0
                    self.terrain_damage(obj)
                    self.check_on_goal(obj)
                    return
        if self.dy < 0:
            # 上方向の衝突判定
            for obj in self.map.map_objects:
                if self.rect.colliderect(obj.rect):
                    self.rect.top = obj.rect.bottom
                    self.dy = 0
                    self.check_on_goal(obj)
                    return

    def _collide_left_right(self):
        if self.dx > 0:
            # 右方向の衝突判定
            for obj in self.map.map_objects:
                if self.rect.colliderect(obj.rect):
                    self.rect.right = obj.rect.left
                    self.dx = 0
                    self.check_on_goal(obj)
                    return
        if self.dx < 0:
            # 左方向の衝突判定
            for obj in self.map.map_objects:
                if self.rect.colliderect(obj.rect):
                    self.rect.left = obj.rect.right
                    self.dx = 0
                    self.check_on_goal(obj)
                    return

    def _on_ground(self):
        # プレイヤーが地面に接しているかどうかを判定する
        self.rect.y += 1
        for obj in self.map.map_objects:
            if self.rect.colliderect(obj.rect):
                self.rect.y -= 1
                return True
        self.rect.y -= 1
        return False

    # プレイヤーが落ちたとき
    def fall(self):
        if self.rect.y > settings.HEIGHT:
            self.hp = 0

    # ダメージ床の処理
    def terrain_damage(self, obj):
        self.hp -= obj.damage

    # ゴールに到達したかどうかの判定
    def check_on_goal(self, obj):
        if obj.is_goal:
            self.is_clear = True
