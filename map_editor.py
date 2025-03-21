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


class Notification:
    """Displays temporary notification messages on the screen"""

    def __init__(self, surface):
        self.surface = surface
        self.messages = []  # List of (message, creation_time, duration, color)
        self.font = FontManager.get_font(24)
        self.padding = 10
        self.default_duration = 3000  # milliseconds
        self.fade_time = 500  # milliseconds to fade out
        self.background_alpha = 180  # transparency of background
        self.max_width = 600  # maximum width for notification

    def add(self, message, duration=None, color=None):
        """Add a notification to display"""
        if duration is None:
            duration = self.default_duration
        if color is None:
            color = settings.COLORS["white"]

        self.messages.append({
            "text": message,
            "start_time": pygame.time.get_ticks(),
            "duration": duration,
            "color": color
        })

    def draw(self):
        """Draw all active notifications"""
        current_time = pygame.time.get_ticks()
        messages_to_keep = []

        for i, message in enumerate(self.messages):
            # Calculate time elapsed
            elapsed = current_time - message["start_time"]

            # Remove expired messages
            if elapsed > message["duration"]:
                continue

            # Calculate opacity for fade out effect
            remaining = message["duration"] - elapsed
            opacity = 255
            if remaining < self.fade_time:
                opacity = int(255 * remaining / self.fade_time)

            # Calculate Y position (stack notifications from bottom up)
            rendered_text = self.font.render(
                message["text"], True, message["color"])
            text_width = min(rendered_text.get_width(), self.max_width)
            text_height = rendered_text.get_height()

            # Create background surface with proper size
            bg_rect = pygame.Rect(
                self.surface.get_width() // 2 - text_width // 2 - self.padding,
                self.surface.get_height() - 100 - (i * (text_height + self.padding * 3)),
                text_width + self.padding * 2,
                text_height + self.padding * 2
            )

            # Draw background with transparency
            bg_surface = pygame.Surface(
                (bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, self.background_alpha * opacity // 255))
            self.surface.blit(bg_surface, bg_rect)

            # Draw text
            text_surface = pygame.Surface(
                rendered_text.get_size(), pygame.SRCALPHA)
            text_surface.blit(rendered_text, (0, 0))
            text_surface.set_alpha(opacity)

            self.surface.blit(text_surface, (
                bg_rect.x + self.padding,
                bg_rect.y + self.padding
            ))

            # Add message to keep list
            messages_to_keep.append(message)

        # Update message list with only active messages
        self.messages = messages_to_keep


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
        self.notification = Notification(surface)

    def _load_map_list(self):
        maps = []
        base_path = os.path.dirname(__file__)
        maps_dir = os.path.join(base_path, "maps")

        # Create maps directory if it doesn't exist
        if not os.path.exists(maps_dir):
            os.makedirs(maps_dir)
            self.notification.add("マップディレクトリを作成しました", color=settings.COLORS["green"])

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
                    error_msg = f"マップ読み込みエラー: {filename}"
                    print(f"{error_msg}: {e}")
                    self.notification.add(
                        error_msg, color=settings.COLORS["red"])

        # If no maps exist, add a placeholder for new map
        if not maps:
            maps.append({
                "filename": "new_map.json",
                "map_name": "新規マップ",
                "filepath": os.path.join(maps_dir, "new_map.json"),
                "is_new": True
            })
            self.notification.add(
                "マップが見つかりません。新しいマップを作成してください。", color=settings.COLORS["yellow"])

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
            self.notification.draw()
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
        self.surface.blit(instructions, (settings.WIDTH // 2 - instructions.get_width() // 2, 100))

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
            pygame.draw.rect(self.surface, button_color, button_rect, border_radius=5)
            pygame.draw.rect(self.surface, settings.COLORS["white"], button_rect, 2, border_radius=5)

            # Map name text
            text = self.font.render(
                map_info["map_name"], True, settings.COLORS["white"])
            self.surface.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

            # Filename text (smaller, below map name)
            filename_text = self.small_font.render(
                map_info["filename"], True, settings.COLORS["white"])
            self.surface.blit(filename_text, (button_rect.centerx - filename_text.get_width() // 2, button_rect.centery + text.get_height() // 2 + 5))


class MapEditor:
    def __init__(self):
        pygame.init()

        # Define header and footer heights
        self.header_height = 50
        self.footer_height = 80

        # Calculate new window size with header and footer
        self.window_width = settings.WIDTH
        self.window_height = settings.HEIGHT + self.header_height + self.footer_height

        # Create the window with the new size
        self.surface = pygame.display.set_mode(
            (self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("マップエディター")

        # Initialize notification system
        self.notification = Notification(self.surface)

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
            self.notification.add(
                "新規マップを作成しました", color=settings.COLORS["green"])
        else:
            self._load_map(selected_map["filepath"])

        self.terrains = []
        self.terrain_color = 1  # 今選択している色
        self.mouse_terrain = None  # マウスが選択している色

        # Create sample terrains for the footer (reordering to put 0 at the end)
        self.terrain_samples = []
        for i in range(1, 10):  # 1-9 terrain types
            self.terrain_samples.append(i)
        self.terrain_samples.append(0)  # Add 0 (empty) as the last item

        self._update_terrains()

    def _load_map(self, filepath):
        try:
            with open(filepath, "r") as f:
                map_data = json.load(f)
                self.map_name = map_data.get("map_name", "名前なし")
                self.map_in_editing = map_data.get("map_data", [])
                print(f"マップを読み込みました: {self.map_name}")
                self.notification.add(
                    f"マップを読み込みました: {self.map_name}", color=settings.COLORS["green"])
        except Exception as e:
            error_msg = f"マップ読み込みエラー: {filepath.split('/')[-1]}"
            print(f"{error_msg}: {e}")
            self.notification.add(error_msg, color=settings.COLORS["red"])

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

        # マウスが選択している色のTerrainを作成 (accounting for header offset)
        x, y = pygame.mouse.get_pos()
        y -= self.header_height  # Adjust for header
        grid_x = int(x / settings.GRID_SIZE)
        grid_y = int(y / settings.GRID_SIZE)

        # Make sure coordinates are valid for terrain creation
        if 0 <= grid_x < settings.WIDTH // settings.GRID_SIZE and 0 <= grid_y < settings.HEIGHT // settings.GRID_SIZE:
            self.mouse_terrain = Terrain(
                self.surface, grid_x, grid_y, self.terrain_color
            )
        else:
            # Create a terrain outside the visible area if mouse is outside
            self.mouse_terrain = Terrain(
                self.surface, -1, -1, self.terrain_color
            )

    def _draw(self):
        # Fill the entire window with black
        self.surface.fill(settings.COLORS["black"])

        # Draw header
        header_rect = pygame.Rect(0, 0, self.window_width, self.header_height)
        pygame.draw.rect(self.surface, settings.COLORS["gray"], header_rect)
        pygame.draw.line(self.surface, settings.COLORS["white"], (0, self.header_height), (self.window_width, self.header_height), 2)

        # Draw header text with Japanese font
        font = FontManager.get_font(24)
        name_text = font.render(
            f"編集中: {self.map_name}", True, settings.COLORS["white"])
        save_text = font.render("Sキー: 保存", True, settings.COLORS["white"])
        self.surface.blit(name_text, (10, 10))
        self.surface.blit(save_text, (self.window_width - save_text.get_width() - 10, 10))

        # Draw footer
        footer_top = self.header_height + settings.HEIGHT
        footer_rect = pygame.Rect(
            0, footer_top, self.window_width, self.footer_height)
        pygame.draw.rect(self.surface, settings.COLORS["gray"], footer_rect)
        pygame.draw.line(self.surface, settings.COLORS["white"], (0, footer_top), (self.window_width, footer_top), 2)

        # Draw terrain chips in the footer
        chip_size = 40
        chip_spacing = 20
        start_x = (self.window_width - (len(self.terrain_samples) * (chip_size + chip_spacing) - chip_spacing)) // 2

        # Draw title for the terrain samples
        sample_title = font.render(
            "マップチップ一覧 (クリックまたは数字キーで選択)", True, settings.COLORS["white"])
        self.surface.blit(sample_title, (self.window_width // 2 - sample_title.get_width() // 2, footer_top + 5))

        # Get mouse position to check for hover effects
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw each terrain chip sample
        for i, terrain_id in enumerate(self.terrain_samples):
            x_pos = start_x + i * (chip_size + chip_spacing)
            y_pos = footer_top + 35

            # Create chip rectangle for hover detection
            chip_rect = pygame.Rect(x_pos, y_pos, chip_size, chip_size)
            is_hovered = chip_rect.collidepoint(mouse_x, mouse_y)

            # Draw highlight for hovering
            if is_hovered:
                hover_rect = pygame.Rect(x_pos - 4, y_pos - 4, chip_size + 8, chip_size + 8)
                pygame.draw.rect(
                    self.surface, settings.COLORS["yellow"], hover_rect, 2, border_radius=2)

            # Draw the terrain chip
            if terrain_id > 0:  # For non-empty terrain
                # Create a small surface for the terrain
                terrain_surface = pygame.Surface((chip_size, chip_size))
                terrain_surface.fill(settings.COLORS["black"])

                # Create a temporary terrain for visualization
                temp_terrain = Terrain(terrain_surface, 0, 0, terrain_id)
                temp_terrain.rect.width = chip_size
                temp_terrain.rect.height = chip_size
                temp_terrain.draw()

                # Draw the terrain on the main surface
                self.surface.blit(terrain_surface, (x_pos, y_pos))
            else:
                # For empty terrain (0), just draw a border
                empty_rect = pygame.Rect(x_pos, y_pos, chip_size, chip_size)
                pygame.draw.rect(
                    self.surface, settings.COLORS["white"], empty_rect, 1)

            # Draw number below the terrain
            number_text = font.render(
                str(terrain_id), True, settings.COLORS["white"])
            self.surface.blit(number_text, (x_pos + chip_size // 2 - number_text.get_width() // 2, y_pos + chip_size + 5))

            # Highlight the current selection
            if terrain_id == self.terrain_color:
                select_rect = pygame.Rect(x_pos - 2, y_pos - 2, chip_size + 4, chip_size + 4)
                pygame.draw.rect(self.surface, settings.COLORS["red"], select_rect, 2)

        # Now draw the actual map in the middle section (offset by header height)
        # Save the original surface position to restore it later
        original_pos = {}
        for obj in self.terrains:
            original_pos[obj] = obj.rect.y
            obj.rect.y += self.header_height
            obj.draw()
            obj.rect.y = original_pos[obj]  # Restore original position

        # Draw the mouse terrain with header offset
        if self.mouse_terrain:
            original_mouse_y = self.mouse_terrain.rect.y
            self.mouse_terrain.rect.y += self.header_height
            self.mouse_terrain.draw()
            self.mouse_terrain.rect.y = original_mouse_y  # Restore original position

        # Draw notifications after everything else
        self.notification.draw()

    def _handle_footer_click(self, x, y):
        """Handle clicks in the footer area to select terrain types"""
        chip_size = 40
        chip_spacing = 20
        start_x = (self.window_width - (len(self.terrain_samples) * (chip_size + chip_spacing) - chip_spacing)) // 2

        footer_top = self.header_height + settings.HEIGHT
        y_pos = footer_top + 35

        for i, terrain_id in enumerate(self.terrain_samples):
            x_pos = start_x + i * (chip_size + chip_spacing)
            chip_rect = pygame.Rect(x_pos, y_pos, chip_size, chip_size)

            if chip_rect.collidepoint(x, y):
                self.terrain_color = terrain_id
                self.notification.add(
                    f"マップチップ {terrain_id} を選択しました", duration=1000, color=settings.COLORS["yellow"])
                return

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

                # Check if click is in the footer area
                footer_top = self.header_height + settings.HEIGHT
                if footer_top <= y < footer_top + self.footer_height:
                    # Handle terrain selection via footer clicks
                    self._handle_footer_click(x, y)
                else:
                    # Adjust y coordinate to account for header
                    y -= self.header_height

                    # Only process clicks within the map area
                    if 0 <= y < settings.HEIGHT:
                        grid_x = x // settings.GRID_SIZE
                        grid_y = y // settings.GRID_SIZE

                        # Make sure we don't go out of bounds
                        if (0 <= grid_y < len(self.map_in_editing) and 0 <= grid_x < len(self.map_in_editing[0])):
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
            self.notification.add("マップディレクトリを作成しました", color=settings.COLORS["green"])

        # Use existing filepath if editing an existing map, otherwise create a new one
        save_path = self.current_filepath if self.current_filepath else os.path.join(
            maps_dir, "new_map.json")

        try:
            with open(save_path, "w") as f:
                json.dump({
                    "map_name": self.map_name,
                    "map_data": self.map_in_editing
                }, f, ensure_ascii=False, indent=4)

            filename = save_path.split('/')[-1]
            success_msg = f"マップを保存しました: {filename}"
            print(success_msg)
            self.notification.add(success_msg, color=settings.COLORS["green"])

            # Update current filepath if this was a new map
            if self.is_new_map:
                self.is_new_map = False
                self.current_filepath = save_path

        except Exception as e:
            error_msg = "保存エラー"
            print(f"{error_msg}: {e}")
            self.notification.add(error_msg, color=settings.COLORS["red"])


if __name__ == "__main__":
    me = MapEditor()
    me.run()
