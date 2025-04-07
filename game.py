import pygame
import settings
from stage import Stage
from title_screen import TitleScreen
import pygame_music_materials as pmm


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(settings.TITLE)
        self.stage_state_number = 0
        self.stage = None
        self.is_title_screen = True
        self.title_screen = TitleScreen(self.surface)

        # 音楽の初期化
        self.mixer = pmm.Mixer()
        self.mixer.set_volume(1.0)
        self.mixer.play(pmm.night)  # タイトル画面の音楽を再生

        self.stage_init()

    def stage_init(self):
        self.stage = Stage(
            self.surface, settings.STAGE_FILE_NAMES[self.stage_state_number], self.mixer)

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
                        self.mixer.play(pmm.field)  # ステージBGMに切り替え

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
                self.is_title_screen = True
                self.mixer.play(pmm.night)  # タイトル画面BGMに戻る
            self.stage_init()
