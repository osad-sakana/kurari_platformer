import pygame
import settings

PLAYER_HP_POSITION = (10, 60)
STAGE_NAME_POSITION = (10, 10)


class UI():
    def __init__(self, surface, player, map):
        self.surface = surface
        self.font = pygame.font.Font("./timemachine-wa.ttf", 30)
        self.player = player
        self.map = map

    def draw(self):
        self.draw_player_ui()
        self.draw_stage_name()

    def draw_player_ui(self):
        hp_text = self.font.render(
            f"HP: {self.player.hp}/{self.player.max_hp}",
            True,
            settings.COLORS["white"]
        )
        self.surface.blit(hp_text, PLAYER_HP_POSITION)

    def draw_stage_name(self):
        stage_name = self.map.map_data["map_name"]
        stage_name_text = self.font.render(
            f"{stage_name}",
            True,
            settings.COLORS["white"]
        )
        self.surface.blit(stage_name_text, STAGE_NAME_POSITION)
