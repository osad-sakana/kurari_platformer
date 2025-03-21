import pygame
import settings
import os
import json
from terrain import Terrain


class FontManager:
    """Japanese font manager to ensure proper rendering of Japanese text"""

    FONT_FILE = "timemachine-wa.ttf"

    @classmethod
    def get_font(cls, size):
        """Get a Japanese font of the specified size"""
        base_path = os.path.dirname(__file__)
        font_path = os.path.join(base_path, cls.FONT_FILE)

        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except Exception as e:
                print(f"フォント読み込みエラー: {e}")
        else:
            print(f"フォントファイルが見つかりません: {font_path}")

        # Fallbacks if the font file couldn't be loaded
        try:
            # Try some common Japanese fonts
            for font_name in ['msgothic', 'meiryo', 'yu gothic', 'hiragino kaku gothic']:
                try:
                    return pygame.font.SysFont(font_name, size)
                except Exception:
                    pass

            # Last resort: default font
            return pygame.font.SysFont(None, size)
        except Exception as e:
            print(f"フォント読み込みエラー: {e}")
            return pygame.font.SysFont(None, size)


class MapSelectionUI:
    def __init__(self, surface):
        self.surface = surface
        # Use local Japanese font
        self.font = FontManager.get_font(36)
        self.small_font = FontManager.get_font(24)
        self.maps = self._load_map_list()
        self.selected_index = 0
        self.running = True
        # UI dimensions
        self.button_height = 50
        self.button_width = 400
        self.button_spacing = 10
        self.instruction_text = "↑↓: 選択   ENTER: 編集   N: 新規作成   ESC: 終了"

    def _load_map_list(self):
        maps = []
        base_path = os.path.dirname(__file__)
        maps_dir = os.path.join(base_path, "maps")

        # Create maps directory if it doesn't exist
        if not os.path.exists(maps_dir):
            os.makedirs(maps_dir)

        for filename in os.listdir(maps_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(maps_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        map_data = json.load(f)
                        maps.append({
                            "filename": filename,
                            "map_name": map_data.get("map_name", "名前なし"),
                            "filepath": file_path
                        })
                except Exception as e:
                    print(f"Error loading map {filename}: {e}")

        # If no maps exist, add a placeholder for new map
        if not maps:
            maps.append({
                "filename": "new_map.json",
                "map_name": "新規マップ",
                "filepath": os.path.join(maps_dir, "new_map.json"),
                "is_new": True
            })

        return maps

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_UP:
                        self.selected_index = max(0, self.selected_index - 1)
                    if event.key == pygame.K_DOWN:
                        self.selected_index = min(
                            len(self.maps) - 1, self.selected_index + 1)
                    if event.key == pygame.K_n:
                        # Create new map
                        return {"is_new": True, "filepath": None}
                    if event.key == pygame.K_RETURN:
                        selected_map = self.maps[self.selected_index]
                        if "is_new" in selected_map:
                            return {"is_new": True, "filepath": None}
                        return selected_map

            self._draw()
            pygame.display.update()

    def _draw(self):
        self.surface.fill(settings.COLORS["black"])

        # Draw title
        title = self.font.render(
            "マップエディター - マップ選択", True, settings.COLORS["white"])
        self.surface.blit(
            title, (settings.WIDTH // 2 - title.get_width() // 2, 50))

        # Draw instructions
        instructions = self.small_font.render(
            self.instruction_text, True, settings.COLORS["white"])
        self.surface.blit(instructions, (settings.WIDTH //
                          2 - instructions.get_width() // 2, 100))

        # Draw map buttons
        start_y = 150
        for i, map_info in enumerate(self.maps):
            y_pos = start_y + i * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(
                settings.WIDTH // 2 - self.button_width // 2,
                y_pos,
                self.button_width,
                self.button_height
            )

            # Button background
            button_color = settings.COLORS["green"] if i == self.selected_index else settings.COLORS["gray"]
            pygame.draw.rect(self.surface, button_color,
                             button_rect, border_radius=5)
            pygame.draw.rect(
                self.surface, settings.COLORS["white"], button_rect, 2, border_radius=5)

            # Map name text
            text = self.font.render(
                map_info["map_name"], True, settings.COLORS["white"])
            self.surface.blit(text, (button_rect.centerx - text.get_width() //
                              2, button_rect.centery - text.get_height() // 2))

            # Filename text (smaller, below map name)
            filename_text = self.small_font.render(
                map_info["filename"], True, settings.COLORS["white"])
            self.surface.blit(filename_text,
                              (button_rect.centerx - filename_text.get_width() // 2, button_rect.centery + text.get_height() // 2 + 5))


class MapEditor:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("マップエディター")

        # Show map selection UI
        self.selection_ui = MapSelectionUI(self.surface)
        selected_map = self.selection_ui.run()

        # Exit if the user closed the selection UI
        if selected_map is None:
            self.should_run = False
            return

        self.should_run = True
        self.is_new_map = selected_map.get("is_new", False)
        self.current_filepath = None if self.is_new_map else selected_map["filepath"]
        self.map_name = "新しいマップ" if self.is_new_map else selected_map["map_name"]

        # Initialize or load map data
        if self.is_new_map:
            self.map_in_editing = []
            for _ in range(int(settings.HEIGHT / settings.GRID_SIZE)):
                tmp_map_list = []
                for _ in range(int(settings.WIDTH / settings.GRID_SIZE)):
                    tmp_map_list.append(0)
                self.map_in_editing.append(tmp_map_list)
        else:
            self._load_map(selected_map["filepath"])

        self.terrains = []
        self.terrain_color = 1  # 今選択している色
        self.mouse_terrain = None  # マウスが選択している色

        self._update_terrains()

    def _load_map(self, filepath):
        try:
            with open(filepath, "r") as f:
                map_data = json.load(f)
                self.map_name = map_data.get("map_name", "名前なし")
                self.map_in_editing = map_data.get("map_data", [])
                print(f"マップを読み込みました: {self.map_name}")
        except Exception as e:
            print(f"マップ読み込みエラー: {e}")
            # Create empty map if loading fails
            self.map_in_editing = []
            for _ in range(int(settings.HEIGHT / settings.GRID_SIZE)):
                tmp_map_list = []
                for _ in range(int(settings.WIDTH / settings.GRID_SIZE)):
                    tmp_map_list.append(0)
                self.map_in_editing.append(tmp_map_list)

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

        # Draw current map name and instructions using Japanese font
        font = FontManager.get_font(24)
        name_text = font.render(
            f"編集中: {self.map_name}", True, settings.COLORS["white"])
        save_text = font.render("Sキー: 保存", True, settings.COLORS["white"])
        self.surface.blit(name_text, (10, 10))
        self.surface.blit(save_text, (10, 40))

    def run(self):
        if not self.should_run:
            return

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
                # Make sure we don't go out of bounds
                if 0 <= grid_y < len(self.map_in_editing) and 0 <= grid_x < len(self.map_in_editing[0]):
                    self.map_in_editing[grid_y][grid_x] = self.terrain_color
            self._update_terrains()

            self._draw()
            pygame.display.update()

    def _save_map(self):
        base_path = os.path.dirname(__file__)
        maps_dir = os.path.join(base_path, "maps")

        # Create maps directory if it doesn't exist
        if not os.path.exists(maps_dir):
            os.makedirs(maps_dir)

        # Use existing filepath if editing an existing map, otherwise create a new one
        save_path = self.current_filepath if self.current_filepath else os.path.join(
            maps_dir, "new_map.json")

        try:
            with open(save_path, "w") as f:
                json.dump({
                    "map_name": self.map_name,
                    "map_data": self.map_in_editing
                }, f, ensure_ascii=False, indent=4)
            print(f"マップを保存しました: {save_path}")
        except Exception as e:
            print(f"保存エラー: {e}")


if __name__ == "__main__":
    me = MapEditor()
    me.run()
