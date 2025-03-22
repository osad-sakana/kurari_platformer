import pygame
import settings

PLAYER_HP_POSITION = (10, 60)
STAGE_NAME_POSITION = (10, 10)
# HP Bar constants
HP_BAR_POSITION = (10, 60)
HP_BAR_SIZE = (200, 20)
HP_BAR_BORDER_WIDTH = 2
# HP Bar color constants
HP_COLOR_MAX = (0, 255, 0)  # Green for max health
HP_COLOR_MIN = (255, 0, 0)  # Red for low health


class UI():
    def __init__(self, surface, player, map):
        self.surface = surface
        self.font = pygame.font.Font(f"./{settings.FONT_FILE_NAME}", 30)
        self.player = player
        self.map = map

    def draw(self):
        self.draw_player_ui()
        self.draw_stage_name()

    def draw_player_ui(self):
        # Draw HP bar background (empty bar)
        pygame.draw.rect(
            self.surface,
            settings.COLORS["white"],
            (HP_BAR_POSITION, HP_BAR_SIZE),
            HP_BAR_BORDER_WIDTH
        )

        # Calculate filled portion of the bar
        hp_ratio = self.player.hp / self.player.max_hp
        fill_width = int(hp_ratio * (HP_BAR_SIZE[0] - 2 * HP_BAR_BORDER_WIDTH))

        # Calculate gradient color based on HP ratio
        r = int(HP_COLOR_MIN[0] * (1 - hp_ratio) + HP_COLOR_MAX[0] * hp_ratio)
        g = int(HP_COLOR_MIN[1] * (1 - hp_ratio) + HP_COLOR_MAX[1] * hp_ratio)
        b = int(HP_COLOR_MIN[2] * (1 - hp_ratio) + HP_COLOR_MAX[2] * hp_ratio)
        bar_color = (r, g, b)

        # Draw the filled portion of the HP bar with gradient color
        if fill_width > 0:
            pygame.draw.rect(
                self.surface,
                bar_color,
                (
                    HP_BAR_POSITION[0] + HP_BAR_BORDER_WIDTH,
                    HP_BAR_POSITION[1] + HP_BAR_BORDER_WIDTH,
                    fill_width,
                    HP_BAR_SIZE[1] - 2 * HP_BAR_BORDER_WIDTH
                )
            )

    def draw_stage_name(self):
        stage_name = self.map.map_data["map_name"]
        stage_name_text = self.font.render(
            f"{stage_name}",
            True,
            settings.COLORS["white"]
        )
        self.surface.blit(stage_name_text, STAGE_NAME_POSITION)
