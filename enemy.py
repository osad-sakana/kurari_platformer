import pygame
import settings


class Enemy:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed_y = 0
        self.speed_x = 0.5  # 横移動の速度
        self.gravity = 0.2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = settings.COLORS["red"]
        self.is_on_ground = False
        self.direction = 1  # 1: 右, -1: 左
        self.jump_power = -5  # ジャンプ力
        self.jump_distance = 100  # ジャンプで進める距離

    def can_reach_other_side(self, map, direction):
        # 仮想的にジャンプして、向こう岸にたどり着けるかチェック
        test_x = self.x
        test_y = self.y
        test_speed_y = self.jump_power
        test_speed_x = self.speed_x * direction

        for _ in range(self.jump_distance):
            # 横移動
            test_x += test_speed_x
            test_rect = pygame.Rect(test_x, test_y, self.width, self.height)

            # 地形との衝突判定
            for terrain in map.map_objects:
                if pygame.Rect.colliderect(test_rect, terrain.rect):
                    return False

            # 重力による落下
            test_speed_y += self.gravity
            test_y += test_speed_y

            # 地面に着地したかチェック
            test_rect.y = test_y
            for terrain in map.map_objects:
                if pygame.Rect.colliderect(test_rect, terrain.rect):
                    return True

        return False

    def update(self, map, player):
        # プレイヤーの方向を常に更新
        if player.rect.x > self.x:
            self.direction = 1
        else:
            self.direction = -1

        if not self.is_on_ground:
            # ジャンプ中の横移動
            self.x += self.speed_x * self.direction
            self.rect.x = self.x

            # 重力による落下
            self.speed_y += self.gravity
            self.y += self.speed_y
            self.rect.y = self.y

            # 地形との衝突判定
            for terrain in map.map_objects:
                if pygame.Rect.colliderect(self.rect, terrain.rect):
                    # ブロックの上に乗る
                    self.y = terrain.rect.top - self.height
                    self.rect.y = self.y
                    self.speed_y = 0
                    self.is_on_ground = True
                    break
        else:
            # 横移動
            self.x += self.speed_x * self.direction
            self.rect.x = self.x

            # 地形との衝突判定（横移動時）
            is_blocked = False
            for terrain in map.map_objects:
                if pygame.Rect.colliderect(self.rect, terrain.rect):
                    # ブロックにぶつかったら反対方向に移動
                    self.direction *= -1
                    self.x += self.speed_x * self.direction
                    self.rect.x = self.x
                    is_blocked = True
                    break

            # 地面との衝突判定（落下防止）
            is_on_ground = False
            self.rect.y += 1  # 1ピクセル下に移動して地面チェック
            for terrain in map.map_objects:
                if pygame.Rect.colliderect(self.rect, terrain.rect):
                    is_on_ground = True
                    break
            self.rect.y -= 1  # 元の位置に戻す

            if not is_on_ground or (is_blocked and self.can_reach_other_side(map, self.direction)):
                # 地面がない場合や、ブロックにぶつかって向こう岸にたどり着ける場合はジャンプ
                self.speed_y = self.jump_power
                self.is_on_ground = False

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def is_out_of_screen(self):
        return self.y > settings.HEIGHT
