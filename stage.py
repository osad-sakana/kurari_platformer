from player import Player
from map import Map
from ui import UI
from background import Background


class Stage:
    def __init__(self, surface, stage_file_name):
        self.surface = surface
        self.map = Map(self.surface)
        self.player = None
        self.ui = None
        self.stage_file_name = stage_file_name
        self.is_clear = False
        self.background = Background(self.surface)
        self.mixer = None
        self.reset()

    # マップの初期化
    def reset(self):
        self.map.load_map(self.stage_file_name)
        self.player = Player(self.surface, self.map, (30, 30))
        self.ui = UI(self.surface, self.player, self.map)

    def update(self):
        self.player.update()
        if self.player.hp <= 0:
            self.reset()
        if self.player.is_clear:
            self.is_clear = True

    def draw(self):
        self.background.draw()
        self.map.draw()
        self.player.draw()
        self.ui.draw()
