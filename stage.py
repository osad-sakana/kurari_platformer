from player import Player
from map import Map
from ui import UI
from background import Background
from enemy import Enemy
import random
import pygame
import settings
import pygame_music_materials as pmm


class Stage:
    def __init__(self, surface, stage_file_name, mixer, sound_manager):
        self.surface = surface
        self.map = Map(self.surface)
        self.player = None
        self.ui = None
        self.stage_file_name = stage_file_name
        self.is_clear = False
        self.background = Background(self.surface)
        self.mixer = mixer
        self.sound_manager = sound_manager
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 60  # 60フレームごとに敵を生成
        self.clear_timer = 0  # クリア後の時間を計測するタイマー
        self.clear_delay = 200  # クリア音楽が鳴り終わるまでの待機フレーム数（約2秒）
        self.is_clearing = False  # クリア演出中かどうか
        self.reset()

    # マップの初期化
    def reset(self):
        self.map.load_map(self.stage_file_name)
        self.player = Player(self.surface, self.map,
                             (30, 30), self.sound_manager)
        self.ui = UI(self.surface, self.player, self.map)
        self.enemies = []
        self.clear_timer = 0
        self.is_clearing = False
        self.is_clear = False

    def spawn_enemy(self):
        x = random.randint(0, settings.WIDTH - 20)
        y = -20  # 画面外から開始
        self.enemies.append(Enemy(self.surface, x, y))

    def update(self):
        # クリア演出中なら
        if self.is_clearing:
            self.clear_timer += 1
            if self.clear_timer >= self.clear_delay:
                self.is_clear = True  # ステージクリアフラグを立てる
            return

        self.player.update()

        # 敵の更新
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0

        for enemy in self.enemies[:]:
            enemy.update(self.map, self.player)  # playerを渡す
            if enemy.is_out_of_screen():
                self.enemies.remove(enemy)
            elif pygame.Rect.colliderect(enemy.rect, self.player.rect):
                self.player.hp -= 1  # HPを1減らす
                self.sound_manager.play("damage")  # ダメージ効果音の再生
                self.enemies.remove(enemy)

        if self.player.hp <= 0:
            self.reset()
        if self.player.is_clear and not self.is_clearing:
            self.start_clear_sequence()

    def start_clear_sequence(self):
        """クリア演出を開始する"""
        self.sound_manager.play("clear")  # クリア効果音の再生
        # クリア音楽を再生（もしpmm.clearが存在する場合）
        try:
            self.mixer.play(pmm.stage_clear)
        except (AttributeError, NameError) as e:
            print(f"クリア音楽を再生できませんでした: {e}")
        self.is_clearing = True  # クリア演出中フラグを立てる
        self.clear_timer = 0

    def draw(self):
        self.background.draw()
        self.map.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player.draw()
        self.ui.draw()
