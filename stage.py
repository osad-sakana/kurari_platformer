from player import Player
from map import Map


class Stage:
    def __init__(self, surface):
        self.surface = surface
        self.player = Player(self.surface)
        self.map = Map(self.surface)
        self.map.load_map("stage0.json")

    def update(self):
        self.player.update()

    def draw(self):
        self.map.draw()
        self.player.draw()
