import pygame
import settings
import os
import json
from terrain import Terrain


class MapEditor:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("マップエディター")

        self.map_in_editing = []
        for _ in range(int(settings.HEIGHT / settings.GRID_SIZE)):
            tmp_map_list = []
            for _ in range(int(settings.WIDTH / settings.GRID_SIZE)):
                tmp_map_list.append(0)
            self.map_in_editing.append(tmp_map_list)

        self.terrains = []

        self.terrain_color = 1  # 今選択している色
        self.mouse_terrain = None  # マウスが選択している色

        self._update_terrains()

    def _update_terrains(self):
        # map_in_editingを元にterrainsを更新する
        self.terrains = []
        for y, row in enumerate(self.map_in_editing):
            for x, cell in enumerate(row):
                if cell == 0:  # 0は何もないタイル
                    continue
                terrain = Terrain(
                    self.surface, x, y, cell
                )
                self.terrains.append(terrain)

        # マウスが選択している色のTerrainを作成
        x, y = pygame.mouse.get_pos()
        grid_x = int(x / settings.GRID_SIZE)
        grid_y = int(y / settings.GRID_SIZE)
        self.mouse_terrain = Terrain(
            self.surface, grid_x, grid_y, self.terrain_color
        )

    def _draw(self):
        self.surface.fill(settings.COLORS["black"])
        for obj in self.terrains:
            obj.draw()
        self.mouse_terrain.draw()

    def run(self):
        while True:
            self.clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.terrain_color = 1
                    if event.key == pygame.K_2:
                        self.terrain_color = 2
                    if event.key == pygame.K_3:
                        self.terrain_color = 3
                    if event.key == pygame.K_4:
                        self.terrain_color = 4
                    if event.key == pygame.K_5:
                        self.terrain_color = 5
                    if event.key == pygame.K_6:
                        self.terrain_color = 6
                    if event.key == pygame.K_7:
                        self.terrain_color = 7
                    if event.key == pygame.K_8:
                        self.terrain_color = 8
                    if event.key == pygame.K_9:
                        self.terrain_color = 9
                    if event.key == pygame.K_0:
                        self.terrain_color = 0
                    if event.key == pygame.K_s:
                        self._save_map()
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                grid_x = x // settings.GRID_SIZE
                grid_y = y // settings.GRID_SIZE
                self.map_in_editing[grid_y][grid_x] = self.terrain_color
            self._update_terrains()

            self._draw()
            pygame.display.update()

    def _save_map(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "maps", "new_map.json")
        with open(file_path, "w") as f:
            json.dump({
                "map_name": "新しいマップ",
                "map_data": self.map_in_editing
            }, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    me = MapEditor()
    me.run()
